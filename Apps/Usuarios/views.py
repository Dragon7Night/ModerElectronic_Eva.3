from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

# IMPORTACION DE forms Y models
from .forms import ClienteSignUpForm, AdminSignUpForm
from .models import ClaveAcceso, Usuario

# Autenticación y vistas basadas en clases
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView



class CrearCuentaView(CreateView):
    form_class = ClienteSignUpForm
    success_url = reverse_lazy("iniciarSesion")
    template_name = "usuario/ingreso/crear_cuenta.html"


class IniciarSesionView(LoginView):
    form_class = AuthenticationForm
    template_name = "usuario/ingreso/iniciar_sesion.html"
    redirect_authenticated_user = True



class CrearCuentaViewAdmin(CreateView):
    form_class = AdminSignUpForm
    success_url = reverse_lazy("iniciarSesion")
    template_name = "usuario/ingreso/crear_cuenta.html"


# VISTA/usuarios

def registroAdmin(request):
    form = AdminSignUpForm()

    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)

        if form.is_valid():
            # Obtener la clave de administrador desde cleaned_data
            clave_pura = form.cleaned_data.get('admin_key')

            # Verificar la clave contra las entradas de ClaveAcceso
            claves = ClaveAcceso.objects.all()
            clave_valida = False

            for clave_objeto in claves:
                if clave_objeto.verificarClave(clave_pura):
                    clave_valida = True
                    break

            if clave_valida:
                # Guardar el usuario como administrador
                user = form.save(commit=False)
                user.rol = Usuario.ROL_ADMIN
                user.is_staff = True
                user.save()
                return HttpResponseRedirect(reverse('iniciarSesion'))
            else:
                # Si la clave es inválida, volver al formulario con error simple en el contexto
                form.add_error('admin_key', 'Clave de administrador inválida')
    
    data = {
        'formKey': form,
        'mainTitle': 'Registro de Administradores',
        'txtBtn': 'Registrar Administrador',
        'colorBg': 'text-bg-danger'
    }
    return render(request, "usuarios/register_admin.html", data)