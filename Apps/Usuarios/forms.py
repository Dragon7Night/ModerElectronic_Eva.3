from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class ClienteSignUpForm(UserCreationForm):
    nombre = forms.CharField(max_length=50)
    direccion = forms.CharField(max_length=90)
    billetera = forms.FloatField(initial=0.0)

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'email', 'nombre', 'direccion', 'billetera')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nombre = self.cleaned_data['nombre']
        user.direccion = self.cleaned_data['direccion']
        user.billetera = self.cleaned_data['billetera']
        user.rol = Usuario.ROL_CLIENTE
        user.is_staff = False
        if commit:
            user.save()
        return user

class AdminSignUpForm(UserCreationForm):
    nombre = forms.CharField(max_length=50)
    admin_key = forms.CharField(max_length=64)

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'email', 'nombre', 'admin_key')

    def clean_admin_key(self):
        clave = self.cleaned_data['admin_key']
        # validar con ClaveAcceso o con cadena
        if clave != "CLAVE_SECRETA":
            raise forms.ValidationError("Clave de administrador incorrecta.")
        return clave

    def save(self, commit=True):
        user = super().save(commit=False) # commit evita volver al form cliente 
        user.nombre = self.cleaned_data['nombre']
        user.rol = Usuario.ROL_ADMIN
        user.is_staff = True
        # ↓↓↓ si se quiere crear un superuser:
        # user.is_superuser = True
        if commit:
            user.save()
        return user

