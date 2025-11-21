
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
    path("crearCuentaCliente/", usuarioViews.CrearCuentaViewCliente.as_view(), name="crearCuentaCliente"),
    path("iniciarSesionCliente/", usuarioViews.IniciarSesionViewCliente.as_view(), name="iniciarSesionCliente"),

    # ----------------------------
    #   -URLs ingreso de admin
    # ----------------------------
    path("crearCuentaAdmin/", usuarioViews.CrearCuentaViewAdmin.as_view(), name="crearCuentaAdmin"),
    path("iniciarSesionAdmin/", usuarioViews.IniciarSesionViewAdmin.as_view(), name="iniciarSesionAdmin"),

    # ----------------------------
    #   -URLs de los perfiles
    # ----------------------------
    path("perfil/", usuarioViews.PerfilUsuarioDetailView.as_view(), name="perfilUsuario"), 
    path("perfil/editar/", usuarioViews.PerfilUsuarioUpdateView.as_view(), name="editarPerfilUsuario"),
]