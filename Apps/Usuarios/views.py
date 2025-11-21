from django.urls import reverse_lazy

# IMPORTACION DE forms Y models
from .forms import ClienteSignUpForm, AdminSignUpForm
from .models import Usuario

# Autenticación y vistas basadas en clases
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView



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

    def form_valid(self, form):
        # 1. El form.save() por defecto llama a create_user o create_superuser si usas UserCreationForm
        # y ya hashea la contraseña.
        self.object = form.save() 
        
        # 2. Una vez que el objeto se ha guardado, actualizamos sus atributos.
        self.object.rol = Usuario.ROL_ADMIN
        self.object.is_staff = True
        self.object.is_superuser = True # Un admin real debería ser superuser

        # 3. Llamamos a save() nuevamente solo para actualizar los campos.
        self.object.save(update_fields=["rol", "is_staff", "is_superuser"])
        
        return super().form_valid(form)

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





