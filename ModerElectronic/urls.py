"""
URL configuration for ModerElectronic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from Apps.Productos import views as productoViews


urlpatterns = [
    path('admin/', admin.site.urls),
    path("usuarios/", include("Apps.Usuarios.urls")),
    path('cuenta/', include("django.contrib.auth.urls")),
    path('', productoViews.homeGeneral, name='homeGeneral' ),

    # -----------------------
    # URLs de Productos
    # -----------------------
    path('data_Producto', productoViews.data_Producto, name='data_Producto'),
    path('register_Producto', productoViews.register_Producto, name='productoRegisterName'),
    path('editar_producto/<int:id_producto>', productoViews.editar_producto, name='productoEditarName'),
    path('eliminar_producto/<int:id_producto>', productoViews.eliminar_producto, name='productoEliminarName'),
    
    # -----------------------
    # URLs de Calificación
    # -----------------------
    path('agregar_Calificacion/<int:id_producto>', productoViews.agregar_Calificacion, name='RegisterCalificacionName'),
    path('data_Calificacion', productoViews.data_Calificacion, name='data_Calificacion'),

    # -----------------------
    # URLs de Solicitud
    # -----------------------
    path('register_Solicitud/<int:id_producto>', productoViews.register_Solicitud, name='RegisterSolicitudName'),
    path('data_Solicitud', productoViews.data_Solicitud, name='data_SolicitudName'),

]
