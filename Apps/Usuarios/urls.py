
from django.urls import path
from .views import *

urlpatterns = [
    path("registroUsuario/",CrearCuentaView.as_view(), name="crearCuenta"),
    path("registroUsuario/",CrearCuentaViewAdmin.as_view(), name="crearCuentaAdmin"),
    path("ingresoUsuario/",IniciarSesionView.as_view(), name="iniciarSesion")
]