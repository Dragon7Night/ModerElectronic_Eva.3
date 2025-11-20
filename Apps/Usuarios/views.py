from django.urls import reverse_lazy

# IMPORTACION DE forms Y models
from .forms import ClienteSignUpForm, AdminSignUpForm
from .models import Usuario

# Autenticación y vistas basadas en clases
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView



class CrearCuentaView(CreateView):
    form_class = ClienteSignUpForm # Formulario personalizado
    success_url = reverse_lazy("iniciarSesion") # redireccionamiento 
    template_name = "usuario/ingreso/crear_cuenta.html" # ubicacion del template


class IniciarSesionView(LoginView):
    form_class = AuthenticationForm
    template_name = "usuario/ingreso/iniciar_sesion.html"
    redirect_authenticated_user = False


class CrearCuentaViewAdmin(CreateView):
    form_class = AdminSignUpForm
    success_url = reverse_lazy("iniciarSesion")
    template_name = "usuario/ingreso/crear_cuenta.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.rol = Usuario.ROL_ADMIN
        user.is_staff = True
        user.save()
        return super().form_valid(form)