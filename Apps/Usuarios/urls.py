
from django.urls import path
from .views import *

urlpatterns = [
    path("crearCuenta/", CrearCuentaView.as_view(), name="crearCuenta"),
    path("crearCuentaAdmin/", CrearCuentaViewAdmin.as_view(), name="crearCuentaAdmin"),
    path("iniciarSesion/", IniciarSesionView.as_view(), name="iniciarSesion"),
]