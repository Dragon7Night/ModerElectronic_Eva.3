
# '======[Importaciones]============================'
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Count # filtros
from django.templatetags.static import static

#   -------------------------------MODELS & FORMS IMPORTS--------------------------------------------
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
    # 1. Consulta Base
    productos_list = ProductoModel.Producto.objects.all().order_by('-fecha_registro')

    # 2. Filtros
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

    # 3. Ordenamiento
    order = request.GET.get('order')
    if order == 'precio_asc':
        productos_list = productos_list.order_by('precio')
    elif order == 'precio_desc':
        productos_list = productos_list.order_by('-precio')

    # 4. Paginación (12 por página)
    paginator = Paginator(productos_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 5. Procesar imágenes (Usando la función auxiliar)
    _procesar_imagenes(page_obj)

    # 6. Datos de categorías para el sidebar
    categorias = ProductoModel.Categoria.objects.annotate(contador_productos=Count('productocategoria'))

    # 7. Mantener filtros en la URL
    params = request.GET.copy()
    if 'page' in params: 
        del params['page']
    base_params = params.urlencode()

    data = {
        'productoKey': page_obj,
        'categoriasKey': categorias,
        'mainTitle': 'Catálogo de productos',
        'base_params': base_params,
    }
    return render(request, 'Producto/catalogo_producto.html', data)

# .|----------------[REGISTRAR PRODUCTO]----------------|.

def registrar_producto(request):
    formProducto = ProductoForm.RegisterProductoForm() 
    
    if request.method == 'POST':
        formProducto = ProductoForm.RegisterProductoForm(request.POST)
        if formProducto.is_valid():
            # Guardar Producto
            producto_instance = formProducto.save()
            
            # Guardar Relación Muchos a Muchos (Categorías)
            categorias_seleccionadas = formProducto.cleaned_data.get('categoria_id')
            
            # Limpiamos relaciones previas (por seguridad) y creamos las nuevas
            ProductoModel.ProductoCategoria.objects.filter(producto_id=producto_instance).delete()
            
            for categoria in categorias_seleccionadas:
                 ProductoModel.ProductoCategoria.objects.create(
                     producto_id=producto_instance, 
                     categoria_id=categoria
                 )
            
            return HttpResponseRedirect(reverse('catalogoProductos'))
    
    # Mostrar últimos 5 productos registrados
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

def editar_producto(request, id_producto):
    # Obtiene el producto o lanza error 404 si no existe
    producto = get_object_or_404(ProductoModel.Producto, id=id_producto)
    
    if request.method == 'POST':
        form = ProductoForm.RegisterProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto_instance = form.save(commit=False)
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

def eliminar_producto(request, id_producto):
    producto = get_object_or_404(ProductoModel.Producto, id=id_producto)
    producto.delete()
    return HttpResponseRedirect(reverse('catalogoProductos'))

# ====↓↓↓↓ EN OBRAS AUN ==========================================================================================

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
    producto = get_object_or_404(ProductoModel.Producto, id=id_producto)
        
    if request.method == 'POST':
        form_calificacion = ProductoForm.RegisterCalificacionForm(request.POST) 
        form_comentario = ProductoForm.RegisterComentarioForm(request.POST)
        
        if form_calificacion.is_valid() and form_comentario.is_valid():
            calif_instance = form_calificacion.save()
            coment_instance = form_comentario.save()

            # Crear relaciones
            ProductoModel.CalificacionProducto.objects.create(
                calificacion_id=calif_instance, producto_id=producto
            )
            ProductoModel.ComentarioProducto.objects.create(
                comentario_id=coment_instance, producto_id=producto
            )
            return HttpResponseRedirect(reverse('catalogoProductos'))
    else:
        form_calificacion = ProductoForm.RegisterCalificacionForm()
        form_comentario = ProductoForm.RegisterComentarioForm()
    
    data = {
        'formCalificacionKey': form_calificacion, 
        'formComentarioKey': form_comentario, 
        'mainTitle': 'Registro de calificaciones',
        'txtBtn': 'Registrar calificación',
        'id_producto': id_producto
    }
    return render(request, 'Valoraciones/estrellas.html', data)


def data_Calificacion(request):
    calificacionObject = ProductoModel.Calificacion.objects.all()
    data = {
         'calificacionKey': calificacionObject,
         'mainTitle': 'Registro de calificaciones',
    }
    return render(request, 'Valoraciones/data_estrellas.html', data)


def register_Solicitud(request, id_producto):
    producto = get_object_or_404(ProductoModel.Producto, id=id_producto)
    
    if request.method == 'POST':
        form_solicitud = ProductoForm.RegisterSolicitudForm(request.POST) 
        if form_solicitud.is_valid():
            solicitud = form_solicitud.save(commit=False)
            solicitud.producto_id = producto 
            solicitud.estado = True  # Asumiendo True por defecto
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