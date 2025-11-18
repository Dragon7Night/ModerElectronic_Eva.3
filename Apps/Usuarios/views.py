from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

# IMPORTACION DE forms Y models
from .forms import ClienteSignUpForm, AdminSignUpForm
from .models import ClaveAcceso, Usuario


# VISTA/usuarios

def homeUsuarios(request):
    return render(request, 'Usuarios/registro/base_registro.html')

def registroCliente(request):

    form = ClienteSignUpForm()

    if request.method == 'POST':
        form = ClienteSignUpForm(request.POST)

        if form.is_valid():
            # Guardar el formulario (asigna automáticamente el rol de Cliente)
            form.save()
            return HttpResponseRedirect(reverse('loginName'))
    
    data = {
        'formKey': form,
        'mainTitle': 'Registro de Clientes',
        'txtBtn': 'Registrar Cliente',
        'colorBg': 'text-bg-primary'
    }
    return render(request, "usuarios/register.html", data)


def registroAdmin(request):

    form = AdminSignUpForm()

    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)

        if form.is_valid():
            # Obtener la clave de administrador antes de guardar (Sin usar .pop())
            clave_pura = form.cleaned_data.get('admin_key')
            
            # 1. Verificar la clave de administrador
            claves = ClaveAcceso.objects.all()
            clave_valida = False
            
            # Bucle simple para verificar la clave (reemplaza 'any' complejo)
            for clave_objeto in claves:
                if clave_objeto.verificarClave(clave_pura):
                    clave_valida = True
                    break  # Salir del bucle si encuentra una clave válida

            if clave_valida:
                # Si la clave es válida, guardar el usuario como administrador
                user = form.save(commit=False)
                user.rol = Usuario.ROL_ADMIN
                user.is_staff = True          # Dar acceso al panel de Django Admin
                user.save()
                return HttpResponseRedirect(reverse('loginName'))
                
            else:
                # Si es inválida, redirigir al home
                return HttpResponseRedirect(reverse('home'))

                

    data = {
        'formKey': form,
        'mainTitle': 'Registro de Administradores',
        'txtBtn': 'Registrar Administrador',
        'colorBg': 'text-bg-danger'
    }
    return render(request, "usuarios/register_admin.html", data)