from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, ClaveAcceso

class ClienteSignUpForm(UserCreationForm):
    nombre = forms.CharField(max_length=50, required=False)
    direccion = forms.CharField(max_length=90, required=False)
    billetera = forms.FloatField(required=False, initial=0.0)

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ("username", "email", "nombre", "direccion", "billetera")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nombre = self.cleaned_data.get("nombre", "")
        user.direccion = self.cleaned_data.get("direccion", "")
        user.billetera = self.cleaned_data.get("billetera") or 0.0
        user.rol = Usuario.ROLE_CLIENT
        if commit:
            user.save()
        return user

class AdminSignUpForm(ClienteSignUpForm):
    admin_key = forms.CharField(max_length=64, required=True, help_text="Clave de acceso para registrarse como administrador")

    def clean_admin_key(self):
        return self.cleaned_data["admin_key"]