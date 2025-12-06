
# '======[Importaciones]============================'
from django.urls import path
import Apps.Usuarios.views as usuarioViews
# '================================================='

# °===========================°
#    °URLs -> Usuarios
# °===========================°

urlpatterns = [

    # ----------------------------
    #   -URLs ingreso de cliente
    # ----------------------------
    path("crear-cuenta-cliente/", usuarioViews.CrearCuentaViewCliente.as_view(), name="crearCuentaCliente"),
    path("iniciar-sesion-cliente/", usuarioViews.IniciarSesionViewCliente.as_view(), name="iniciarSesionCliente"),

    # ----------------------------
    #   -URLs ingreso de admin
    # ----------------------------
    path("crear-cuenta-admin/", usuarioViews.CrearCuentaViewAdmin.as_view(), name="crearCuentaAdmin"),
    path("iniciar-sesion-admin/", usuarioViews.IniciarSesionViewAdmin.as_view(), name="iniciarSesionAdmin"),

    # ----------------------------
    #   -URLs de los perfiles
    # ----------------------------
    path("perfil/", usuarioViews.PerfilUsuarioDetailView.as_view(), name="perfilUsuario"), 
    path("perfil/editar/", usuarioViews.PerfilUsuarioUpdateView.as_view(), name="editarPerfilUsuario"),

    # ----------------------------
    #   -URLs de la billetera    
    # ----------------------------
    path("recargar-billetera/", usuarioViews.RecargarBilleteraView.as_view(), name="recargarBilletera"),
    path("seleccionar-metodo/", usuarioViews.SeleccionarMetodoRecargaView.as_view(), name="seleccionarMetodo"),
    path("confirmacion-recarga/", usuarioViews.ConfirmacionRecargaView.as_view(), name="confirmacionRecarga"),

    # ----------------------------
    #   -URLs del historial  
    # ----------------------------
    path('perfil/historial/', usuarioViews.HistorialComprasView.as_view(), name='historialCompras'),

    # ----------------------------
    #   -URLs del baneo   
    # ----------------------------
    path('perfil/Lista/', usuarioViews.ListaClientesAdminView.as_view(), name='listaClientes'),
    path('admin/banear/<int:user_id>/', usuarioViews.banear_cliente_view, name='banear_cliente'),

    path('admin/desbanear/<int:user_id>/', usuarioViews.desbanear_cliente, name='desbanear_cliente'),
]

