
from django.urls import path
import Apps.Usuarios.views as usuarioViews

urlpatterns = [
    path("crearCuentaCliente/", usuarioViews.CrearCuentaViewCliente.as_view(), name="crearCuentaCliente"),
    path("crearCuentaAdmin/", usuarioViews.CrearCuentaViewAdmin.as_view(), name="crearCuentaAdmin"),
    path("iniciarSesionCliente/", usuarioViews.IniciarSesionViewCliente.as_view(), name="iniciarSesionCliente"),
    path("iniciarSesionAdmin/", usuarioViews.IniciarSesionViewAdmin.as_view(), name="iniciarSesionAdmin"),

# --- RUTAS DE PERFIL ---
    path("perfil/", usuarioViews.PerfilUsuarioDetailView.as_view(), name="perfilUsuario"), 
    path("perfil/editar/", usuarioViews.PerfilUsuarioUpdateView.as_view(), name="editarPerfilUsuario"),

]