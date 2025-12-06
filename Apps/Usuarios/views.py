
# '======[Importaciones]============================'
from django.urls import reverse_lazy
from decimal import Decimal

# Django: utilidades y atajos
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

# Django: autenticación
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

# Django: vistas basadas en clases
from django.views.generic import CreateView, DetailView, UpdateView, ListView, TemplateView
from django.views.generic.edit import FormView

# Formularios y modelos
from Apps.Usuarios import forms as UsuariosForms
from Apps.Productos import forms as ProductoForms
from Apps.Usuarios import models as UsuariosModels
from Apps.Productos import models as ProductoModel
# '================================================='

# °===========================°
#    °Vistas -> Usuarios
# °===========================°

# !|-|--|-|-|-|-|-|-|> VISTA BASADAS EN CLASE PARA LA GESTION DE CLIENTES <|-|--|-|-|-|-|-|-|-|-|-|-|-

class CrearCuentaViewCliente(CreateView):
    form_class = UsuariosForms.ClienteSignUpForm # Formulario personalizado
    success_url = reverse_lazy("iniciarSesionCliente") # redireccionamiento 
    template_name = "Usuario/ingreso/crear_cuenta/crear_cliente.html" # ubicacion del template


class IniciarSesionViewCliente(LoginView):
    # form_class = AuthenticationForm
    template_name = "usuario/ingreso/iniciar_sesion/iniciar_cliente.html"
    redirect_authenticated_user = False
    authentication_form = UsuariosForms.VerificacionEstadoCuentaForm


# !|-|--|-|-|-|-|-|-|> VISTA BASADAS EN CLASE PARA LA GESTION DE ADMINISTRADORES <|-|--|-|-|-|-|-|-|-|-|-|-|-

class CrearCuentaViewAdmin(CreateView):
    form_class = UsuariosForms.AdminSignUpForm
    success_url = reverse_lazy("iniciarSesionAdmin")
    template_name = "Usuario/ingreso/crear_cuenta/crear_admin.html"

class IniciarSesionViewAdmin(LoginView):
    form_class = AuthenticationForm
    template_name = "usuario/ingreso/iniciar_sesion/iniciar_admin.html"
    redirect_authenticated_user = False


# !|-|--|-|-|-|-|-|-|> VISTA PARA MOSTRAR EL PERFIL <|-|--|-|-|-|-|-|-|-|-|-|-|-

class PerfilUsuarioDetailView(LoginRequiredMixin, DetailView):
    model = UsuariosModels.Usuario
    template_name = 'Usuario/Perfil/mostrar_perfil.html' # Crea este nuevo template
    context_object_name = 'usuario_perfil' # Nombre de la variable en el template

    # Esta función se asegura de que la vista siempre cargue el usuario logueado.
    def get_object(self, queryset=None):
        return self.request.user

# !|-|--|-|-|-|-|-|-|> VISTA PARA EDITAR EL PERFIL <|-|--|-|-|-|-|-|-|-|-|-|-|-

class PerfilUsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = UsuariosModels.Usuario
    form_class = UsuariosForms.PerfilUsuarioUpdateForm
    template_name = 'Usuario/Perfil/editar_perfil.html' # Crea este nuevo template
    success_url = reverse_lazy('perfilUsuario') # Redirección después de guardar

    # Esta función se asegura de que solo se edite el usuario logueado.
    def get_object(self, queryset=None):
        return self.request.user


# !|-|--|-|-|-|-|-|-|> VISTA PARA LA BILLETERA <|-|--|-|-|-|-|-|-|-|-|-|-|-

class SeleccionarMetodoRecargaView(LoginRequiredMixin, TemplateView):
    template_name = "Billetera/seleccionar_metodo.html"


class RecargarBilleteraView(LoginRequiredMixin, FormView):
    template_name = 'Billetera/recargar_billetera.html' 
    form_class = UsuariosForms.RecargaBilleteraForm
    
    success_url = reverse_lazy('perfilUsuario') 

    def form_valid(self, form):
        monto = form.cleaned_data['monto']
        usuario = self.request.user

        saldo_actual = Decimal(str(usuario.billetera)) if usuario.billetera else Decimal('0.0')

        usuario.billetera = saldo_actual + monto
        usuario.save()

        messages.success(self.request, f"Recarga exitosa. Tu nuevo saldo es: {usuario.billetera}")
        return super().form_valid(form)

 
class ConfirmacionRecargaView(LoginRequiredMixin, TemplateView):
    template_name = "Billetera/confimarcion_recarga.html"

    def get_context_data(self, **kwargs):
        recargar = super().get_context_data(**kwargs)
        recargar["usuario"] = self.request.user
        monto_str = self.request.session.get('ultimo_monto', '0.00')  # recupera el monto
        try:
            monto_decimal = Decimal(monto_str)
        except:
            monto_decimal = Decimal('0.00')
            recargar["monto"]
        return recargar
    

# !|-|--|-|-|-|-|-|-|> VISTA PARA COMPRAS <|-|--|-|-|-|-|-|-|-|-|-|-|-

class HistorialComprasView(LoginRequiredMixin, ListView):
   
    model = ProductoModel.RegistroCompra 
    template_name = 'Usuario/Perfil/historial_compras.html'
    context_object_name = 'registros_compra' 

    def get_queryset(self):
        return ProductoModel.RegistroCompra.objects.filter(cliente=self.request.user).order_by('-fecha_compra')


# !|-|--|-|-|-|-|-|-|> VISTA PARA GESTION DE USUARIOS <|-|--|-|-|-|-|-|-|-|-|-|-|-

class ListaClientesAdminView(ListView):
    model = UsuariosModels.Usuario
    template_name = 'Usuario/Perfil/Lista_clientes.html'
    context_object_name = 'clientes' 

    def get_queryset(self):
        return UsuariosModels.Usuario.objects.filter(rol=UsuariosModels.Usuario.ROL_CLIENTE).order_by('username')
    
def banear_cliente_view(request, user_id):
    baneo_cliente = get_object_or_404(UsuariosModels.Usuario, id=user_id)

    if baneo_cliente.baneo_usuario(reason="Infracción de las políticas de la plataforma"):
        messages.success(request, f"El cliente {baneo_cliente.username} ha sido baneado")
    else:
        messages.error(request, 'No fue posible banear al usuario')
    
    return redirect('listaClientes')

def desbanear_cliente(request, user_id):
    desbaneo_cliente = get_object_or_404(UsuariosModels.Usuario, id=user_id)

    if desbaneo_cliente.desbaneo_usuario():
        messages.success(request, f"El cliente {desbaneo_cliente.username} ha sido desbaneado")
    else:
        messages.error(request, 'No fue posible desbanear al usuario')
    
    return redirect('listaClientes')

