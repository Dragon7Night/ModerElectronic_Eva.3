
# '======[Importaciones]============================'
from django.contrib import admin
from django.urls import path, include

# IMPORTACION DE REDIRECCIONAMIENTO AUTOMATICO 
# .DOC -> https://docs.djangoproject.com/en/5.2/topics/class-based-views/#:~:text=django.views.generic%20import%20TemplateView
from django.views.generic import RedirectView
# '==============================================='

# °===========================°
#    °URLs -> ModerElectronic
# °===========================°

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuenta/', include("django.contrib.auth.urls")),

    # ---------------------------------------
    # -Redireccionamiento automatico al home
    # ---------------------------------------
    path('', RedirectView.as_view(pattern_name='homeGeneral', permanent=False)),

    # -----------------------
    #    -URLs de Usuarios
    # -----------------------
    path("usuarios/", include("Apps.Usuarios.urls")),

    # -----------------------
    #    -URLs de Productos
    # -----------------------
    path("productos/", include("Apps.Productos.urls")),

]






















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