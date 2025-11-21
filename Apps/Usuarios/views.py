
# '======[Importaciones]============================'
from django.urls import reverse_lazy

# IMPORTACION DE forms Y models
from .forms import ClienteSignUpForm, AdminSignUpForm
from .models import Usuario

# Autenticación y vistas basadas en clases
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
# '================================================='

# °===========================°
#    °Vistas -> Usuarios
# °===========================°

# Vistas para el registro e ingreso de clientes
class CrearCuentaViewCliente(CreateView):
    form_class = ClienteSignUpForm # Formulario personalizado
    success_url = reverse_lazy("iniciarSesionCliente") # redireccionamiento 
    template_name = "Usuario/ingreso/crear_cuenta/crear_cliente.html" # ubicacion del template


class IniciarSesionViewCliente(LoginView):
    form_class = AuthenticationForm
    template_name = "usuario/ingreso/iniciar_sesion/iniciar_cliente.html"
    redirect_authenticated_user = False





class CrearCuentaViewAdmin(CreateView):
    form_class = AdminSignUpForm
    success_url = reverse_lazy("iniciarSesionAdmin")
    template_name = "Usuario/ingreso/crear_cuenta/crear_admin.html"


class IniciarSesionViewAdmin(LoginView):
    form_class = AuthenticationForm
    template_name = "usuario/ingreso/iniciar_sesion/iniciar_admin.html"
    redirect_authenticated_user = False


from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PerfilUsuarioUpdateForm # Importa el nuevo formulario

# --- VISTA PARA MOSTRAR EL PERFIL ---
class PerfilUsuarioDetailView(LoginRequiredMixin, DetailView):
    model = Usuario
    template_name = 'Usuario/perfil/mostrar_perfil.html' # Crea este nuevo template
    context_object_name = 'usuario_perfil' # Nombre de la variable en el template

    # Esta función se asegura de que la vista siempre cargue el usuario logueado.
    def get_object(self, queryset=None):
        return self.request.user


# --- VISTA PARA EDITAR EL PERFIL ---
class PerfilUsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = PerfilUsuarioUpdateForm
    template_name = 'Usuario/perfil/editar_perfil.html' # Crea este nuevo template
    success_url = reverse_lazy('perfilUsuario') # Redirección después de guardar

    # Esta función se asegura de que solo se edite el usuario logueado.
    def get_object(self, queryset=None):
        return self.request.user





