from django import forms

# Importa tu modelo de usuario
from .models import Usuario 
# Para manejar el hashing de la contraseña
from django.contrib.auth.forms import UserCreationForm, UserChangeForm



# --- FORMULARIO DE REGISTRO DE CLIENTES ---

class ClienteSignUpForm(UserCreationForm):
    # Campos adicionales no incluidos en UserCreationForm por defecto
    direccion = forms.CharField(max_length=90)
    
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'email', 'direccion') 

    def save(self, commit=True):
        # 1. Llamar a super().save() sin commit=False, ya que UserCreationForm 
        # está diseñado para hacer el hash y guardar la contraseña correctamente.
        user = super().save(commit=True) 
        
        # 2. Actualizar los campos adicionales
        user.direccion = self.cleaned_data['direccion']
        user.rol = Usuario.ROL_CLIENTE
        user.is_staff = False
        user.is_superuser = False
        
        # Se actualizan los campos del cliete con los nuevos valores
        user.save(update_fields=['direccion', 'rol', 'is_staff', 'is_superuser']) 
        return user


# --- 2. FORMULARIO DE REGISTRO DE ADMINISTRADORES ---

class AdminSignUpForm(UserCreationForm):
    admin_key = forms.CharField(max_length=64, label="Clave de Administrador") 

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'email', 'admin_key')

    def clean_admin_key(self):
        clave = self.cleaned_data['admin_key']

        # Validacion de identidad con la clave de acceso
        if clave != "CLAVE_SECRETA": # ¡Recuerdar cambiar "CLAVE_SECRETA" por una clave real!
            raise forms.ValidationError("Clave de administrador incorrecta.")
        return clave

    def save(self, commit=True):
        # 1. Guardamos el usuario. Esto ya hashea la contraseña y crea el objeto.
        # Quitamos commit=False para evitar problemas de contraseña.
        user = super().save(commit=True) 
        
        # 2. Actualizamos los campos de rol y permisos
        user.rol = Usuario.ROL_ADMIN
        user.is_staff = True
        user.is_superuser = True

        # 3. Guardamos los cambios de permisos y rol.
        user.save(update_fields=['rol', 'is_staff', 'is_superuser']) 
        return user


# --- 3. FORMULARIO DE EDICIÓN DE PERFIL ---

class PerfilUsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('email', 'direccion')


