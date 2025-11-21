from django import forms

# Importa tu modelo de usuario
from .models import Usuario 
# Para manejar el hashing de la contraseña
from django.contrib.auth.forms import UserCreationForm, UserChangeForm



# --- 1. FORMULARIO DE REGISTRO DE CLIENTES ---

class ClienteSignUpForm(UserCreationForm):
    # Campos adicionales no incluidos en UserCreationForm por defecto
    nombre = forms.CharField(max_length=50)
    direccion = forms.CharField(max_length=90)
    # Recomendación: Los campos FloatField no son estándar en forms.py
    # Si quieres que se muestre, es mejor usar un DecimalField o dejarlo fuera del formulario de registro.
    # Como lo tienes en el modelo con default=0.0, lo vamos a manejar en el save().
    # Eliminamos billetera del formulario para que use el default del modelo.
    
    class Meta(UserCreationForm.Meta):
        model = Usuario
        # Nota: Si el campo 'billetera' es un FloatField con default=0.0, 
        # puedes excluirlo si no quieres que el usuario lo ingrese al registrarse.
        fields = ('username', 'email', 'direccion') 

    def save(self, commit=True):
        # 1. Llamar a super().save() sin commit=False, ya que UserCreationForm 
        # está diseñado para hacer el hash y guardar la contraseña correctamente.
        user = super().save(commit=True) 
        
        # 2. Actualizar los campos adicionales
        user.direccion = self.cleaned_data['direccion']
        # La billetera ya tiene 0.0 por defecto en el modelo, no es necesario actualizarla.
        user.rol = Usuario.ROL_CLIENTE
        user.is_staff = False
        user.is_superuser = False
        
        # 3. Guardar las actualizaciones de campos (ya que super().save() ya guardó el objeto)
        # Usamos update_fields para ser más eficientes.
        user.save(update_fields=['direccion', 'rol', 'is_staff', 'is_superuser']) 
        return user


# --- 2. FORMULARIO DE REGISTRO DE ADMINISTRADORES ---

class AdminSignUpForm(UserCreationForm):
    nombre = forms.CharField(max_length=50)
    # Campo para la clave secreta de registro
    admin_key = forms.CharField(max_length=64, label="Clave de Administrador") 

    class Meta(UserCreationForm.Meta):
        model = Usuario
        # Excluye 'direccion' y 'billetera' si el admin no las necesita al registrarse.
        fields = ('username', 'email', 'admin_key')

    def clean_admin_key(self):
        clave = self.cleaned_data['admin_key']
        # Validamos con la cadena secreta directamente.
        if clave != "CLAVE_SECRETA": # ¡Recuerda cambiar "CLAVE_SECRETA" por una clave real!
            raise forms.ValidationError("Clave de administrador incorrecta.")
        return clave

    def save(self, commit=True):
        # 1. Guardamos el usuario. Esto ya hashea la contraseña y crea el objeto.
        # Quitamos commit=False para evitar problemas de contraseña.
        user = super().save(commit=True) 
        
        # 2. Actualizamos los campos de rol y permisos
        user.rol = Usuario.ROL_ADMIN
        user.is_staff = True
        user.is_superuser = True # Recomendado para un administrador que usa un formulario especial

        # 3. Guardamos los cambios de permisos y rol.
        user.save(update_fields=['rol', 'is_staff', 'is_superuser']) 
        return user


# --- 3. FORMULARIO DE EDICIÓN DE PERFIL ---

class PerfilUsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        # 'username' es un campo que usualmente no se permite editar
        fields = ('email', 'direccion', 'billetera') 
        # Asegúrate de no incluir campos sensibles como 'password' o 'rol'


