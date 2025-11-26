
# '======[Importaciones]============================'
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator # PAGINAS DINAMICAS
from django.db.models import Count, Avg # CONTADOR DE FILTROS Y AVG (promedio)
from django.templatetags.static import static

from django.contrib import messages # Importante para feedback visual

from django.contrib.auth.decorators import login_required

# ----[MODELS & FORMS IMPORTS]-------------------
from Apps.Productos import models as ProductoModel

from Apps.Productos import forms as ProductoForm
# '================================================='

# °===========================°
#    °Vistas -> Productos
# °===========================°


# CONSTANTE DE LA LISTA DE IMAGENES PARA LAS CATEGORIA
CATEGORIA_IMAGENES = {
    'adaptadores': 'img/CategoriasVec/adaptadores.png',
    'altavoces': 'img/CategoriasVec/altavoces.png',
    'audifonos': 'img/CategoriasVec/audifonos.png',
    'computadoras': 'img/CategoriasVec/computadoras.png',
    'consolas': 'img/CategoriasVec/consolas.png',
    'impresoras': 'img/CategoriasVec/impresoras.png',
    'inalambricos': 'img/CategoriasVec/inalambricos.png',
    'mouse': 'img/CategoriasVec/mouse.png',
    'televisores': 'img/CategoriasVec/televisores.png',
    'teclados': 'img/CategoriasVec/teclados.png',
    'otros': 'img/CategoriasVec/box.png',
}


# ====== FUNCIONES AUXILIARES ======
def _procesar_imagenes(lista_productos):
    """
    Asigna la URL de la imagen de categoría a cada producto en la lista.
    Evita repetir código en las vistas.
    """
    for producto in lista_productos:
        # Obtenemos la primera relación de categoría
        relacion = ProductoModel.ProductoCategoria.objects.filter(producto_id=producto).first()
        
        if relacion:
            nombre_cat = relacion.categoria_id.nombre.lower()
            # Verificamos si existe imagen para esa categoría
            if nombre_cat in CATEGORIA_IMAGENES:
                producto.url_categoria = static(CATEGORIA_IMAGENES[nombre_cat])
            else:
                producto.url_categoria = None
            producto.nombre_categoria = relacion.categoria_id.nombre
        else:
            producto.url_categoria = None
            producto.nombre_categoria = "General"
    return lista_productos

# !|-|--|-|-|-|-|-|-|> VISTAS GENERALES <|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
# Redireccion al HOME principal del proyecto
def homeGeneral(request):
    return render(request, 'index.html')


# !|-|--|-|-|-|-|-|-|> VISTAS DE PRODUCTOS <|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|

# .|----------------[MOSTRAR PRODUCTOS]----------------|.

def catalogo_producto(request):
    # GUARDA TODOS LOS DATOS EN EL OBJETOS odenados por fecha de registro
    productos_list = ProductoModel.Producto.objects.all().order_by('-fecha_registro')

    # FILTROS
    query = request.GET.get('q')
    if query:
        productos_list = productos_list.filter(nombre__icontains=query)

    min_price = request.GET.get('min_price')
    if min_price:
        productos_list = productos_list.filter(precio__gte=min_price)

    max_price = request.GET.get('max_price')
    if max_price:
        productos_list = productos_list.filter(precio__lte=max_price)

    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos_list = productos_list.filter(productocategoria__categoria_id=categoria_id)

    # BOTON SUPERIOR PARA ORDENAR POR PRECIO MAS FALMENTE
    order = request.GET.get('order')
    if order == 'precio_asc':
        productos_list = productos_list.order_by('precio')
    elif order == 'precio_desc':
        productos_list = productos_list.order_by('-precio')

    # PAGINAS PARA LOS PRODUCTOS MOSTRADOS (12 por pagina)
    paginas = Paginator(productos_list, 12)
    num_pagina = request.GET.get('page')
    paginasObject = paginas.get_page(num_pagina)

    # ASIGNACION DE IMAGENES POR LAS CATEGORAS (mediante funcion adicional)
    _procesar_imagenes(paginasObject)

    # Datos de categorías para el sidebar
    categorias = ProductoModel.Categoria.objects.annotate(contador_productos=Count('productocategoria'))

    # Mantener filtros en la URL
    params = request.GET.copy()
    if 'page' in params: 
        del params['page']
    base_params = params.urlencode()

    data = {
        'productoKey': paginasObject,
        'categoriasKey': categorias,
        'mainTitle': 'Catálogo de productos',
        'base_params': base_params,
    }
    return render(request, 'Producto/catalogo_producto.html', data)

""" EN TESTING AUN """
def detalle_producto(request, id_producto):
    # Usamos get_object_or_404 para manejar si el producto no existe
    producto = get_object_or_404(ProductoModel.Producto, id=id_producto)
    
    # Calcular promedio de estrellas
    # 'calificaciones' es el related_name que definimos en models.py
    promedio_calificacion = producto.calificaciones.aggregate(Avg('cant_estrella'))['cant_estrella__avg']
    
    # Formularios vacíos para la vista
    form_comentario = ProductoForm.RegisterComentarioForm()
    form_calificacion = ProductoForm.RegisterCalificacionForm()

    # --- Lógica para obtener la URL de la imagen ---
    # Usamos el campo FK producto_id para el filtro
    relacion = ProductoModel.ProductoCategoria.objects.filter(producto_id=producto).first() 
    
    if relacion:
        nombre_cat = relacion.categoria_id.nombre.lower() # Usamos el campo FK categoria_id
        # Usa el diccionario que definiste arriba
        producto.url_categoria = static(CATEGORIA_IMAGENES.get(nombre_cat)) if nombre_cat in CATEGORIA_IMAGENES else None
        producto.nombre_categoria = relacion.categoria_id.nombre
    else:
        producto.url_categoria = None
        producto.nombre_categoria = "General"
    # --- FIN Lógica para obtener la URL de la imagen ---

    data = {
        'producto': producto,
        'promedio_calificacion': promedio_calificacion,
        'formComentario': form_comentario,
        'formCalificacion': form_calificacion,
        # Usando related_name para obtener los comentarios del producto
        'comentarios': producto.comentarios.all().order_by('-fecha_registro'), 
    }
    return render(request, 'Producto/detalle_producto.html', data)


# .|----------------[AGREGAR FEEDBACK (ESTRELLAS + COMENTARIO)]----------------|.
@login_required(login_url='/login/')
def agregar_feedback(request, id_producto):
    """
    Procesa el formulario de estrellas y comentario enviado desde detalle_producto.
    """
    producto = get_object_or_404(ProductoModel.Producto, id=id_producto)
    
    if request.method == 'POST':
        # Instanciamos los formularios con los datos del POST
        # Nota: Al usar inputs manuales HTML, Django buscará los 'name' coincidentes
        form_com = ProductoForm.RegisterComentarioForm(request.POST)
        form_cal = ProductoForm.RegisterCalificacionForm(request.POST)
        
        # Validamos y Guardamos
        try:
            # 1. Guardar Comentario (si el usuario escribió algo)
            if form_com.is_valid():
                comentario_texto = request.POST.get('comentario', '').strip()
                if comentario_texto: # Solo guardar si no está vacío
                    comentario = form_com.save(commit=False)
                    comentario.cliente = request.user # Corregido: cliente_id -> cliente
                    comentario.producto = producto    # Corregido: producto_id -> producto
                    comentario.save()

            # 2. Guardar Calificación (Estrellas)
            # Verificamos si form_cal es válido O si el dato crudo viene en el POST
            if form_cal.is_valid():
                calificacion = form_cal.save(commit=False)
                calificacion.cliente = request.user
                calificacion.producto = producto
                calificacion.save()
            else:
                # Fallback por si el form validation falla pero el dato existe
                estrellas = request.POST.get('cant_estrella')
                if estrellas:
                    ProductoModel.Calificacion.objects.create(
                        producto=producto,
                        cliente=request.user,
                        cant_estrella=int(estrellas)
                    )
            
            messages.success(request, '¡Gracias por tu calificación!')
            
        except Exception as e:
            messages.error(request, f'Error al guardar tu opinión: {e}')
            
    # Redirigimos al usuario de vuelta a la página de detalle del producto
    return HttpResponseRedirect(reverse('detalleProducto', args=[id_producto]))

# .|----------------[REGISTRAR PRODUCTO]----------------|.

# PERMITE REQUERIR QUE EL USER ESTE LOGEADO (decorador)
@login_required(login_url='/login/')
def registrar_producto(request):
    formProducto = ProductoForm.RegisterProductoForm() 
    
    if request.method == 'POST':
        formProducto = ProductoForm.RegisterProductoForm(request.POST)
        if formProducto.is_valid():
            # Guardar Producto
            producto_instance = formProducto.save(commit=False)
            
            # ASIGNACIÓN DEL ADMIN
            producto_instance.admin = request.user 
            producto_instance.save()
            
            # RELACION MANY TO MANY (Categoria)
            categorias_seleccionadas = formProducto.cleaned_data.get('categoria_id')
            
            # LIMPIEZA DE REFERENCIAS Y CREACION DE NUEVAS (for .. in)
            ProductoModel.ProductoCategoria.objects.filter(producto_id=producto_instance).delete()
            
            for categoria in categorias_seleccionadas:
                 ProductoModel.ProductoCategoria.objects.create(
                     producto_id=producto_instance, 
                     categoria_id=categoria
                 )
            
            return HttpResponseRedirect(reverse('catalogoProductos'))
    
    # MOSTRAR LOS ULTIMOS 5 PRODUCTOS REGISTRADO orden fecha desasendente
    ultimos_productos = ProductoModel.Producto.objects.all().order_by('-fecha_registro')[:5]
    _procesar_imagenes(ultimos_productos)

    data = {
        'formKey': formProducto,
        'mainTitle': 'Registro de productos',
        'txtBtn': 'Registrar producto',
        'ultimos_productos': ultimos_productos,
    }
    return render(request, 'Producto/registrar_producto.html', data)

# .|----------------[EDITAR PRODUCTO]----------------|.

""" EN TESTING AUN """
@login_required(login_url='/login/')
def editar_producto(request, id_producto):

    # OBTIENE EL OBJETO O SI NO UN ERROR 404 (dos en uno)
    producto = get_object_or_404(ProductoModel.Producto, id=id_producto)
    
    if request.method == 'POST':
        form = ProductoForm.RegisterProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto_instance = form.save(commit=False)
            
            # Si el campo admin_id está vacío, se podría reasignar al usuario actual
            if not producto_instance.admin_id:
                producto_instance.admin_id = request.user
                
            producto_instance.save()
            
            # Actualizar Categorías
            categorias_seleccionadas = form.cleaned_data.get('categoria_id')
            ProductoModel.ProductoCategoria.objects.filter(producto_id=producto_instance).delete()
            
            for categoria in categorias_seleccionadas:
                ProductoModel.ProductoCategoria.objects.create(
                    producto_id=producto_instance, 
                    categoria_id=categoria
                )
            return HttpResponseRedirect(reverse('catalogoProductos'))
    else:
        # Pre-llenar el formulario con las categorías actuales
        ids_cats = ProductoModel.ProductoCategoria.objects.filter(producto_id=producto).values_list('categoria_id', flat=True)
        form = ProductoForm.RegisterProductoForm(instance=producto, initial={'categoria_id': ids_cats})

    data = {
        'formKey': form,
        'txtBtn': 'Editar producto',
        'mainTitle': 'Edición de Producto'
    }
    return render(request, 'Producto/registrar_producto.html', data)



# .|----------------[ELIMINAR PRODUCTO]----------------|.

""" EN TESTING AUN """
# PERMITE REQUERIR QUE EL USER ESTE LOGEADO (decorador)
@login_required(login_url='/login/')
def eliminar_producto(request, id_producto):

    # OBTIENE EL OBJETO O SI NO UN ERROR 404 (dos en uno)
    producto = get_object_or_404(ProductoModel.Producto, id=id_producto)
    producto.delete()
    return HttpResponseRedirect(reverse('catalogoProductos'))


# !|-|--|-|-|-|-|-|-|> VISTAS DE CATEGORIAS <|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|

# .|----------------[MOSTRAR CATEGORIAS]----------------|.
def data_categoria(request):
    categoriaObject = ProductoModel.Categoria.objects.all()
    data = {
        'categoriaKey': categoriaObject,
        'mainTitle': 'Listado de categorías',
    }
    return render(request, 'ModerElectronic/data_Categoria.html', data)

# .|----------------[REGISTRAR CATEGORIAS]----------------|.

# PERMITE REQUERIR QUE EL USER ESTE LOGEADO (decorador)
@login_required(login_url='/login/')
def registrar_categoria(request):
    formCategoria = ProductoForm.RegisterCategoriaForm()
    
    if request.method == 'POST':
        formCategoria = ProductoForm.RegisterCategoriaForm(request.POST)
        if formCategoria.is_valid():
            formCategoria.save()
            return HttpResponseRedirect(reverse('registrarProducto')) 
    
    categorias_registradas = ProductoModel.Categoria.objects.all().order_by('nombre')
    
    data = {
        'formKey': formCategoria,
        'mainTitle': 'Registro de Categorías',
        'txtBtn': 'Guardar Categoría',
        'categorias_registradas': categorias_registradas,
    }
    return render(request, 'Producto/Extras/registrar_categoria.html', data)

# -----------------------------------CALIFICACION-------------------------------------------------------


def agregar_Calificacion(request, id_producto):
    return HttpResponseRedirect(reverse('detalleProducto', args=[id_producto])) 

def data_Calificacion(request):
    calificacionObject = ProductoModel.Calificacion.objects.all()
    data = {
         'calificacionKey': calificacionObject,
         'mainTitle': 'Registro de calificaciones',
    }
    return render(request, 'Valoraciones/data_estrellas.html', data)


def register_Solicitud(request, id_producto):

    # OBTIENE EL OBJETO O SI NO UN ERROR 404 (dos en uno)
    producto = get_object_or_404(ProductoModel.Producto, id=id_producto)
    
    if request.method == 'POST':
        form_solicitud = ProductoForm.RegisterSolicitudForm(request.POST) 
        if form_solicitud.is_valid():
            solicitud = form_solicitud.save(commit=False)
            solicitud.producto_id = producto 
            solicitud.cliente_id = request.user # Asumo que el usuario actual es el cliente
            solicitud.estado = True 
            solicitud.tipo_solicitud = 'en revision'
            solicitud.save()
            return HttpResponseRedirect(reverse('catalogoProductos'))
    else:
        form_solicitud = ProductoForm.RegisterSolicitudForm()
        
    data= {
        'formSolicitudKey': form_solicitud, 
        'mainTitle': 'Registrar solicitud',
        'txtBtn': 'Guardar solicitud',
        'id_producto': id_producto
    }
    return render(request, 'Usuario/Solicitud/solicitud.html', data)


def data_Solicitud(request):
    solicitudObject = ProductoModel.Solicitud.objects.all()
    data = {
        'solicitudKey': solicitudObject,
        'mainTitle': 'Registro de solicitudes',
    }
    return render(request, 'Usuario/Solicitud/data_solicitud.html', data)
