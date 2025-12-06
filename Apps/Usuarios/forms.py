
# '======[Importaciones]============================'
from django import forms

from Apps.Usuarios.models import Usuario 

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
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
        
        user.direccion = self.cleaned_data['direccion']
        user.rol = Usuario.ROL_CLIENTE
        user.is_staff = False
        user.is_superuser = False
        user.es_baneado = False

        user.save(update_fields=['direccion', 'rol', 'is_staff', 'is_superuser', 'es_baneado']) 
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


# --- FORMULARIO DE RECARGAR BILLETERA ---
class RecargaBilleteraForm(forms.Form):
    monto = forms.DecimalField(min_value=1, label="Monto a recargar")


# --- FORMULARIO DE AUTENTICACIÓN PERSONALIZADO ---
class VerificacionEstadoCuentaForm(AuthenticationForm):

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            try:
                # SE BUSCA EL CLIENTE EN LA DB POR SU USERNAME
                user = Usuario.objects.get(username=username)
            except Usuario.DoesNotExist:
                # en caso de no existir se muestra error de credenciales invalidas
                pass
            else:
                #Si el usuario existe se verifica el estado (is_active)
                if not user.is_active:
                    # Si esta baneado
                    raise forms.ValidationError(
                        ("Tu cuenta ha sido baneada o desactivada por un administrador. "),
                        code='inactive',
                    )
                # Si el usuario esta activo, se procede con la autenticacion normal de django
            return super().clean()

        # Si faltan campos, llama al clean() original
        return super().clean()

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        
        # mensaje de error personalizado para las credenciales invalidas
        self.error_messages['invalid_login'] = (
            "Nombre de usuario o contraseña incorrectos. Por favor, intentalo de nuevo."
        )
