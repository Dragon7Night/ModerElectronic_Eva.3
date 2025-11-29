
# '======[Importaciones]============================'
from django import forms

from Apps.Usuarios.models import Usuario 

from django.contrib.auth.forms import UserCreationForm
# '================================================='

# °===========================°
#    °Formulario -> Usuarios
# °===========================°

# --- FORMULARIO DE REGISTRO DE CLIENTES ---

class ClienteSignUpForm(UserCreationForm):
    direccion = forms.CharField(max_length=90)
    
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'email', 'direccion') 

    def save(self, commit=True):
        user = super().save(commit=True) 
        
        # Actualizar los campos adicionales
        user.direccion = self.cleaned_data['direccion']
        user.rol = Usuario.ROL_CLIENTE
        user.is_staff = False
        user.is_superuser = False
        
        # Se actualizan los campos del cliete con los nuevos valores
        user.save(update_fields=['direccion', 'rol', 'is_staff', 'is_superuser']) 
        return user


# --- FORMULARIO DE REGISTRO DE ADMINISTRADORES ---

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
        user = super().save(commit=True) 
        
        user.rol = Usuario.ROL_ADMIN
        user.is_staff = True
        user.is_superuser = True

        user.save(update_fields=['rol', 'is_staff', 'is_superuser']) 
        return user


# --- FORMULARIO DE EDICIÓN DE PERFIL ---

class PerfilUsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('email', 'direccion')




