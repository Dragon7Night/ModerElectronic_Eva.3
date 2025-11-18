from django.urls import path



from django.urls import path
from .views import CrearCuentaView, IniciarSesionView

urlpatterns = [
    path("registroUsuario/",CrearCuentaView.as_view(), name="crearCuenta"),
    path("ingresoUsuario/",IniciarSesionView.as_view(), name="iniciarSesion")
]