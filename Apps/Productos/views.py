# from django.shortcuts import render


from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

#correos

#   -------------------------------MODELS & FORMS IMPORTS--------------------------------------------
from Apps.Productos.models import Producto, Categoria, ProductoCategoria, Comentario, ComentarioProducto, Calificacion, CalificacionProducto, Solicitud

from Apps.Productos.forms import RegisterProductoForm, RegisterCategoriaForm, RegisterComentarioForm, RegisterCalificacionForm, RegisterSolicitudForm, RegistroCompra




# Create your views here.


def homeGeneral(request):
    return render(request, 'index.html')




#------------------------------------PRODUCTO-------------------------------------------------------
def data_Producto(request):
    productoObject = Producto.objects.all()
    data = {
        'productoKey':productoObject,
        'mainTitle':'Registro de productos',
        'titulo':'producto registrado',
        'colorBg':'text-bg-success'
    }
    return render(request, 'Producto/data_Producto.html',data)

   

    
def register_Producto(request):
    form = RegisterProductoForm()
    if request.method == 'POST':
        form = RegisterProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('data_Producto'))
        
    data = {
        'formKey':form,
        'mainTitle':'Registro de productos',
        'txtForm':'Formulario de registro de productos',
        'txtBtn':'Registrar producto',
        'colorBg':'text-bg-warning'
    }
    return render(request, 'Producto/registrarProducto.html',data)


def editar_producto(request, id_producto):
    producto = Producto.objects.get(id=id_producto)
    form = RegisterProductoForm(instance=producto)

    if request.method == 'POST':
        form = RegisterProductoForm(request.POST, instance=producto)
    if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('data_Producto'))

    data = {
        'formKey':form,
        'txtForm':'Formulario de edicion de productos',
        'txtBtn':'Editar producto',
        'colorBg':'text-bg-warning'
    }
    return render(request, 'Productos/registrar_Producto.html',data)

def eliminar_producto(request, id_producto):
    productoObjects = Producto.objects.get(id=id_producto)
    productoObjects.delete()
    return HttpResponseRedirect(reverse('data_Producto'))

#------------------------------------CATEGORIA-------------------------------------------------------

def data_Categoria(request):
    categoriaObject = Categoria.objects.all()
    data = {
        'categoriaKey':categoriaObject,
        'mainTitle':'Registro de categorias',
        'titulo':'categoria registrado',
        'colorBg':'text-bg-success'
    }
    return render(request, 'ModerElectronic/data_Categoria.html',data)



# #------------------------------------CALIFICACION-------------------------------------------------------

def data_Calificacion(request):
    calificacionObject = Calificacion.objects.all()
    data = {
         'calificacionKey':calificacionObject,
         'mainTitle':'Registro de calificaciones',
         'titulo':'calificacion registrado',
         'colorBg':'text-bg-success'
    }
    return render(request, 'Valoraciones/data_estrellas.html',data)

def agregar_Calificacion(request, id_producto):
    try:
        producto_instance = Producto.objects.get(id=id_producto)  #Intentara obtener el id recibido en la URL
    except Producto.DoesNotExist:
        return HttpResponseRedirect(reverse('data_Producto')) # si no existe lo dirige a data
        
        
    if request.method == 'POST':
        form_calificacion = RegisterCalificacionForm(request.POST) 
        form_comentario = RegisterComentarioForm(request.POST) #tanto el de arriba y abajo verifica que ambos formularios contengan datos validos.
#
        if form_calificacion.is_valid() and form_comentario.is_valid():

            calificacion_instance = form_calificacion.save() #guardamos los datos tanto de calificacion y el comentario en sus respectivas tablas
            comentario_instance = form_comentario.save() 

            CalificacionProducto.objects.create(
                calificacion_id=calificacion_instance,
                producto_id=producto_instance
            )
            ComentarioProducto.objects.create(
                comentario_id=comentario_instance,
                producto_id=producto_instance
            )
#creamos registros que relacionan calificacion y comentario de un producto
            return HttpResponseRedirect(reverse('data_Producto'))

        form_calificacion_con_error = form_calificacion
        form_comentario_con_error = form_comentario

# se guardan los formulacios con errores para mostrarlos nuevamente en el template
    else:
        form_calificacion_con_error = RegisterCalificacionForm()
        form_comentario_con_error = RegisterComentarioForm()

#se crean formularios vacíos para mostrarlos en la plantilla permitiendo asi ingresar datos
    
    data= {

        'formCalificacionKey': form_calificacion_con_error, 
        'formComentarioKey': form_comentario_con_error, 
        'mainTitle': 'Registro de calificaciones',
        'txtForm': 'Formulario de registro de calificaciones',
        'txtBtn': 'Registrar calificacion',
        'colorBg': 'text-bg-warning',
        'id_producto': id_producto
    }

    # preparamos un diccionario con los datos y formularios que se enviaran al html
    return render(request, 'Valoraciones/estrellas.html', data)



# #------------------------------------SOLICITUD-------------------------------------------------------

def data_Solicitud(request):
    solicitudObject = Solicitud.objects.all()
    data = {
        'solicitudKey':solicitudObject,
        'mainTitle':'Registro de solicitudes',
        'titulo':'solicitud registrado',
        'colorBg':'text-bg-success'
    }
    return render(request, 'Usuario/Solicitud/data_solicitud.html',data)



def register_Solicitud(request, id_producto):
    try:
        producto_instance = Producto.objects.get(id=id_producto) 
    except Producto.DoesNotExist:
        return HttpResponseRedirect(reverse('data_Producto')) 
    if request.method == 'POST':
        form_solicitud = RegisterSolicitudForm(request.POST) 
        if form_solicitud.is_valid():
# DE AQUI PARA ABAJO ES NUEVO "nuevooo"
            solicitud_instance = form_solicitud.save(commit=False) #con esto creamos sin guardarlo en la base de datos
            solicitud_instance.producto_id = producto_instance #asignamos el producti el cual pertenece la solicitud    
            solicitud_instance.estado = 'True' #con esto establecemos el estado de la soli
            solicitud_instance.tipo_solicitud = 'esperando' #tipo de solicitud
            solicitud_instance.save()
            return HttpResponseRedirect(reverse('data_Producto'))
    else:
        form_solicitud = RegisterSolicitudForm()
    data= {

        'formSolicitudKey': form_solicitud, 
        'mainTitle': 'Registrar solicitud',
        'txtBtn': 'guardar solicitud',
        'colorBg': 'text-bg-warning',
        'id_producto': id_producto
    }
    return render(request, 'Usuario/Solicitud/solicitud.html', data)


