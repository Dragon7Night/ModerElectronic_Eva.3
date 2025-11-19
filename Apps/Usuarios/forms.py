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
        if commit:
            user.save()
        return user
    

class AdminSignUpForm(ClienteSignUpForm):
    admin_key = forms.CharField(max_length=64, help_text="Ingrese la clave de acceso")

    def clean_admin_key(self):
        clave = self.cleaned_data['admin_key']
        if clave != "CLAVE_SECRETA":
            raise forms.ValidationError("Clave de administrador incorrecta.")
        return clave

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = Usuario.ROL_ADMIN
        if commit:
            user.save()
        return user
