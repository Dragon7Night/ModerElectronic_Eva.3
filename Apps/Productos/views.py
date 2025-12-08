
# '======[Importaciones]============================'
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator # PAGINAS DINAMICAS
from django.db.models import Count, Avg # CONTADOR DE FILTROS Y AVG (promedio)
from django.templatetags.static import static

from decimal import Decimal

from django.contrib import messages # Importante para calificacion visual

from django.contrib.auth.decorators import login_required, permission_required

# ----[MODELS & FORMS IMPORTS]-------------------
from Apps.Productos import models as ProductoModel
from Apps.Usuarios import models as UsuarioModels
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
    'inalambrico': 'img/CategoriasVec/inalambricos.png',
    'mouse': 'img/CategoriasVec/mouse.png',
    'televisores': 'img/CategoriasVec/televisores.png',
    'teclados': 'img/CategoriasVec/teclados.png',
    'otros': 'img/CategoriasVec/box.png',
}




# ====== FUNCION AUXILIAR ======
def _procesar_imagenes(lista_productos):
    """
    Asigna la URL de la imagen de categoria a cada producto en la lista
    """
    for producto in lista_productos:
        # Obtenemos la primera relación de categoría
        relacion = ProductoModel.ProductoCategoria.objects.filter(producto_id=producto).first()
        
        if relacion:
            nombre_cat = relacion.categoria_id.nombre.lower()
            # Verificar si existe un imagen para la categoria capturada
            if nombre_cat in CATEGORIA_IMAGENES:
                producto.url_categoria = static(CATEGORIA_IMAGENES[nombre_cat])
            else:
                producto.url_categoria = None
            producto.nombre_categoria = relacion.categoria_id.nombre
        else:
            producto.url_categoria = None
            producto.nombre_categoria = "Otras"
    return lista_productos

# !|-|--|-|-|-|-|-|-|> VISTAS GENERALES <|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
# Redireccion al HOME principal del proyecto
def homeGeneral(request):
    return render(request, 'index.html')


# !|-|--|-|-|-|-|-|-|> VISTAS DE PRODUCTOS <|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|

# .|----------------[MOSTRAR PRODUCTOS]----------------|.

# .|======== CATALOGO DE PRODUCTOS ==============>>
@login_required(login_url='/productos/home/') # <- DECORADOR que obliga a los usuarios a estar logeados
def catalogo_producto(request):

    productos_list = ProductoModel.Producto.objects.all().order_by('nombre')
    
    # --------||=--== FILTROS ==--=||--------
    # Buscar por ID
    busqueda_id = request.GET.get('busqueda_id')
    if busqueda_id:
        if busqueda_id.isdigit(): 
            productos_list = productos_list.filter(id=busqueda_id)
        else:
            productos_list = productos_list.none()

    # Buscar por NOMBRE
    busqueda_nombre = request.GET.get('busqueda_nombre')
    if busqueda_nombre:
        productos_list = productos_list.filter(nombre__icontains=busqueda_nombre)

    # Buscar por RANGOS de PRECIOS
    precio_min = request.GET.get('precio_min')
    if precio_min:
        productos_list = productos_list.filter(precio__gte=precio_min)

    precio_max = request.GET.get('precio_max')
    if precio_max:
        productos_list = productos_list.filter(precio__lte=precio_max)

    # Buscar por CARTEGORIAS
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos_list = productos_list.filter(productocategoria__categoria_id=categoria_id)

    # ORGANIZACION POR PRECIO
    orden = request.GET.get('orden')
    if orden == 'precio_asc':
        productos_list = productos_list.order_by('precio')
    elif orden == 'precio_desc':
        productos_list = productos_list.order_by('-precio')

    # PAGINACION
    paginas = Paginator(productos_list, 12)
    num_pagina = request.GET.get('page')
    paginasObject = paginas.get_page(num_pagina)


    # --||=--== CLASIFICAION de IMAGENES por NOMBRES ==--=||--------
    for producto in paginasObject:
        relacion = ProductoModel.ProductoCategoria.objects.filter(producto_id=producto.id).first()
        
        if relacion:
            nombre_cat = relacion.categoria_id.nombre
            producto.nombre_categoria = nombre_cat
            
            key_lower = nombre_cat.lower()
            # Validacion de que el diccionario exista y tenga la clave
            if 'CATEGORIA_IMAGENES' in globals() and key_lower in CATEGORIA_IMAGENES:
                 producto.url_categoria = static(CATEGORIA_IMAGENES[key_lower])
            else:
                 producto.url_categoria = None 
        else:
            producto.nombre_categoria = "General"
            producto.url_categoria = None

    # Datos de la SideBar
    categorias = ProductoModel.Categoria.objects.annotate(contador_productos=Count('productocategoria'))

    params = request.GET.copy()
    if 'page' in params: 
        del params['page']
    base_params = params.urlencode()

    data = {
        'productoKey': paginasObject,
        'ultimos_productos': paginasObject,
        'categoriasKey': categorias,
        'base_params': base_params,
    }
    return render(request, 'Producto/catalogo_producto.html', data)


# .|======== DETALLE DE UN PRODUCTO ==============>>

# .|======== DETALLE DE UN PRODUCTO ==============>>

@login_required(login_url='/productos/home/')
def detalle_producto(request, id_producto):
    producto = get_object_or_404(ProductoModel.Producto, id=id_producto)
    
    # Promedio de estrellas
    promedio_calificacion = producto.calificaciones.aggregate(Avg('cant_estrella'))['cant_estrella__avg']
    
    # Traer todas las calificaciones (ya incluyen comentario)
    calificaciones_db = (producto.calificaciones.select_related('cliente').order_by('-fecha_registro'))
    
    lista_opiniones = []
    for cal in calificaciones_db:
        num_estrellas = cal.cant_estrella or 0

        opinion = {
            'cliente': cal.cliente,
            'texto': cal.comentario,
            'fecha': cal.fecha_registro,
            'estrellas': num_estrellas,
            'rango_llenas': range(num_estrellas),
            'rango_vacias': range(5 - num_estrellas),
        }
        lista_opiniones.append(opinion)

    # Info de categoría + imagen
    relacion = ProductoModel.ProductoCategoria.objects.filter(producto_id=producto).first()
    if relacion:
        nombre_cat = relacion.categoria_id.nombre.lower()
        producto.url_categoria = static(CATEGORIA_IMAGENES.get(nombre_cat)) if nombre_cat in CATEGORIA_IMAGENES else None
        producto.nombre_categoria = relacion.categoria_id.nombre
    else:
        producto.url_categoria = None
        producto.nombre_categoria = "Otros"

    # Formulario único para calificación + comentario
    form_calificacion = ProductoForm.RegisterCalificacionForm()

    data = {
        'producto': producto,
        'promedio_calificacion': promedio_calificacion,
        'formCalificacion': form_calificacion,
        'lista_opiniones': lista_opiniones,
    }
    return render(request, 'Producto/detalle_producto.html', data)


# .|----------------[AGREGAR CALIFICACION (ESTRELLAS + COMENTARIO)]----------------|.
@login_required(login_url='/productos/home/')
def agregar_calificacion(request, id_producto):
    producto = get_object_or_404(ProductoModel.Producto, id=id_producto)
    
    if request.method == 'POST':
        # Usamos el formulario unificado
        form_calificacion = ProductoForm.RegisterCalificacionForm(request.POST)
        
        try:
            if form_calificacion.is_valid():
                cant_estrella = form_calificacion.cleaned_data['cant_estrella']
                comentario = form_calificacion.cleaned_data.get('comentario', '').strip()

                # Un solo registro por (producto, cliente)
                ProductoModel.Calificacion.objects.update_or_create(
                    producto=producto,
                    cliente=request.user,
                    defaults={
                        'cant_estrella': cant_estrella,
                        'comentario': comentario,
                    }
                )

                messages.success(request, '¡Gracias por tu opinión!')
            else:
                messages.error(request, 'Por favor corrige los errores del formulario antes de enviar.')
            
        except Exception as err:
            messages.error(request, f'Ocurrió un error al guardar: {err}')
            
    return HttpResponseRedirect(reverse('detalleProducto', args=[id_producto]))



# .|----------------[REGISTRAR PRODUCTO]----------------|.
@login_required(login_url='/productos/home/')
@permission_required(UsuarioModels.Usuario.ROL_ADMIN, login_url='/productos/home/') # <- Requerimiento de rol especifica del User
def registrar_producto(request):
    formProducto = ProductoForm.RegisterProductoForm() 
    
    if request.method == 'POST':
        formProducto = ProductoForm.RegisterProductoForm(request.POST)
        if formProducto.is_valid():
            # Guardar Producto
            producto_instance = formProducto.save(commit=False)
            
            # ASIGNACION DEL ADMIN
            producto_instance.admin = request.user 
            producto_instance.save()
            
            # RELACION MANY TO MANY (Categoria)
            categorias_seleccionadas = formProducto.cleaned_data.get('categoria_id')

            ProductoModel.ProductoCategoria.objects.filter(producto_id=producto_instance).delete()
            
            for categoria in categorias_seleccionadas:
                 ProductoModel.ProductoCategoria.objects.create(
                     producto_id=producto_instance, 
                     categoria_id=categoria
                 )
            
            return HttpResponseRedirect(reverse('catalogoProductos'))
    
    ultimos_productos = ProductoModel.Producto.objects.all().order_by('-fecha_registro')[:5]
    _procesar_imagenes(ultimos_productos)

    data = {
        'formKey': formProducto,
        'ultimos_productos': ultimos_productos,
    }
    return render(request, 'Producto/registrar_producto.html', data)


# .|----------------[EDITAR PRODUCTO]----------------|.
@login_required(login_url='/productos/home/')
@permission_required(UsuarioModels.Usuario.ROL_ADMIN, login_url='/productos/home/')
def editar_producto(request, id_producto):

    # OBTIENE EL OBJETO O SI NO UN ERROR 404 (dos en uno)
    producto = get_object_or_404(ProductoModel.Producto, id=id_producto)
    
    if request.method == 'POST':
        form = ProductoForm.RegisterProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto_instance = form.save(commit=False)
            
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
        ids_cats = ProductoModel.ProductoCategoria.objects.filter(
            producto_id=producto
        ).values_list('categoria_id', flat=True)

        form = ProductoForm.RegisterProductoForm(
            instance=producto,
            initial={'categoria_id': ids_cats}
        )

    data = {
        'formKey': form,
        'producto': producto,
    }

    return render(request, 'Producto/Extras/editar_producto.html', data)


# .|----------------[ELIMINAR PRODUCTO]----------------|.
@login_required(login_url='/productos/home/')
@permission_required(UsuarioModels.Usuario.ROL_ADMIN, login_url='/productos/home/')
def eliminar_producto(request, id_producto):

    # OBTIENE EL OBJETO O SI NO UN ERROR 404 (dos en uno)
    producto = get_object_or_404(ProductoModel.Producto, id=id_producto)
    producto.delete()
    return HttpResponseRedirect(reverse('catalogoProductos'))


# !|-|--|-|-|-|-|-|-|> VISTAS DE CATEGORIAS <|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|

# .|----------------[MOSTRAR CATEGORIAS]----------------|.
@login_required(login_url='/productos/home/')
def data_categoria(request):
    categoriaObject = ProductoModel.Categoria.objects.all()
    data = {
        'categoriaKey': categoriaObject,
    }
    return render(request, 'ModerElectronic/data_Categoria.html', data)


# .|----------------[REGISTRAR CATEGORIAS]----------------|.
@login_required(login_url='/productos/home/')
@permission_required(UsuarioModels.Usuario.ROL_ADMIN, login_url='/productos/home/')
def registrar_categoria(request):
    
    # Query con anotación de cantidad de productos por categoría
    categoriaObject = (
        ProductoModel.Categoria.objects
        .annotate(
            contador_productos=Count(
                'productocategoria__producto_id',
                distinct=True
            )
        )
        .order_by('nombre')
    )

    # Paginador de 10 categorías por página 
    paginator = Paginator(categoriaObject, 10)
    page_number = request.GET.get('page')
    categorias_page = paginator.get_page(page_number)

    # Formulario
    if request.method == 'POST':
        formCategoria = ProductoForm.RegisterCategoriaForm(request.POST)
        if formCategoria.is_valid():
            formCategoria.save()
            return HttpResponseRedirect(reverse('registrarProducto'))
    else:
        formCategoria = ProductoForm.RegisterCategoriaForm()

    data = {
        'formKey': formCategoria,
        'categorias_registradas': categorias_page,
    }
    return render(request, 'Producto/Extras/registrar_categoria.html', data)



# !|-|--|-|-|-|-|-|-|> VISTAS DE SOLICITUDES <|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|

# .|----------------[REGISTRAR SOLICITUD]----------------|.
@login_required(login_url='/productos/home/')
def register_solicitud(request, registro_id):
   
    registro_compra = get_object_or_404(ProductoModel.RegistroCompra, id=registro_id)
    
    if request.method == 'POST':
        form_solicitud = ProductoForm.RegisterSolicitudForm(request.POST) 
        if form_solicitud.is_valid():
            solicitud = form_solicitud.save(commit=False)
            solicitud.producto = registro_compra.producto
            solicitud.registro_compra = registro_compra
            solicitud.cliente = request.user
            solicitud.estado = True 
            solicitud.tipo_solicitud = 'en revision'
            solicitud.save()
            return HttpResponseRedirect(reverse('catalogoProductos'))
    else:
        form_solicitud = ProductoForm.RegisterSolicitudForm()
        
    data = {
        'RegistroCompra': registro_compra,
        'formSolicitudKey': form_solicitud,
        'registro_id': registro_id
    }
    return render(request, 'Usuario/Solicitud/solicitud.html', data)


# .|----------------[MOSTRAR SOLICITUD]----------------|.
@login_required(login_url='/productos/home/')
@permission_required(UsuarioModels.Usuario.ROL_ADMIN, login_url='/productos/home/')
def data_Solicitud(request):
    solicitudes = (
        ProductoModel.Solicitud.objects
        .select_related('cliente', 'producto', 'registro_compra')
        .order_by('-fecha_registro')
    )
    data = {
        'solicitudKey': solicitudes
    }
    return render(request, 'Usuario/Solicitud/data_solicitud.html', data)

# .|----------------[APROBAR SOLICITUD]----------------|.
@login_required(login_url='/productos/home/')
@permission_required(UsuarioModels.Usuario.ROL_ADMIN, login_url='/productos/home/')
def aprobar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(ProductoModel.Solicitud, id=solicitud_id)

    # Evitar procesar dos veces la misma solicitud
    if not solicitud.estado or solicitud.tipo_solicitud != 'en revision':
        messages.warning(request, 'Esta solicitud ya fue gestionada previamente.')
        return redirect('dataSolicitud')

    registro = solicitud.registro_compra
    if registro is None:
        messages.error(
            request,
            'No es posible procesar el reembolso: la solicitud no tiene una compra asociada.'
        )
        return redirect('dataSolicitud')

    cliente = solicitud.cliente
    producto = solicitud.producto

    try:
        monto_reembolso = Decimal(str(registro.precio_total))
        billetera_actual = Decimal(str(cliente.billetera)) if cliente.billetera else Decimal('0.0')
    except Exception as err:
        messages.error(request, f'Error al calcular el reembolso: {err}')
        return redirect('dataSolicitud')

    # 1. Devolver dinero a la billetera
    cliente.billetera = billetera_actual + monto_reembolso
    cliente.save(update_fields=['billetera'])

    # 2. Devolver el producto al stock
    producto.stock = producto.stock + 1
    producto.save(update_fields=['stock'])

    # 3. Actualizar estado de la solicitud
    solicitud.estado = False             # Cerrada
    solicitud.tipo_solicitud = 'aprobada'
    solicitud.save(update_fields=['estado', 'tipo_solicitud'])

    messages.success(
        request,
        f'Solicitud #{solicitud.id} aprobada. '
        f'Se reembolsaron ${monto_reembolso} al cliente {cliente.username} y se devolvió 1 unidad al stock.'
    )
    return redirect('dataSolicitud')


# .|----------------[RECHAZAR SOLICITUD]----------------|.
@login_required(login_url='/productos/home/')
@permission_required(UsuarioModels.Usuario.ROL_ADMIN, login_url='/productos/home/')
def rechazar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(ProductoModel.Solicitud, id=solicitud_id)

    if not solicitud.estado or solicitud.tipo_solicitud != 'en revision':
        messages.warning(request, 'Esta solicitud ya fue gestionada previamente.')
        return redirect('dataSolicitud')

    solicitud.estado = False
    solicitud.tipo_solicitud = 'rechazada'
    solicitud.save(update_fields=['estado', 'tipo_solicitud'])

    messages.info(request,f'Solicitud #{solicitud.id} rechazada. No se realizaron cambios en la compra ni en la billetera.')
    return redirect('dataSolicitud')


# !|-|--|-|-|-|-|-|-|> VISTA DE COMPRA <|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|

# .|----------------[CONFIRMAR COMPRA]----------------|.
@login_required(login_url='/productos/home/')
def confirmar_compra(request, id_producto):
    producto = get_object_or_404(ProductoModel.Producto, id=id_producto)
    cliente = request.user

    try:
        precio_base = Decimal(str(producto.precio))
        billetera_Decimal = Decimal(str(cliente.billetera)) 
    except Exception as erro:
        messages.error(request, f'Error técnico al procesar montos: {erro}')
        return redirect('detalleProducto', id_producto=id_producto)

    # Costos adicionales
    precio_garantia = precio_base * Decimal('0.05')# porcentaje de la garantia extendida
    precio_delivery = Decimal('5000')

    if request.method == 'POST':
        # Checkboxes del formulario
        garantia_extendida = request.POST.get('garantia_extendida') == 'on'
        delivery = request.POST.get('delivery') == 'on'

        precio_total = precio_base

        if garantia_extendida:
            precio_total += precio_garantia

        if delivery:
            precio_total += precio_delivery

        # Validaciones básicas
        if producto.stock <= 0:
            messages.error(request, "¡Lo sentimos! Este producto se ha agotado.")
            return redirect('detalleProducto', id_producto=id_producto)

        if billetera_Decimal < precio_total:
            messages.error(
                request,
                f"Saldo insuficiente. Te faltan ${precio_total - billetera_Decimal} para realizar la compra."
            )
            return redirect('detalleProducto', id_producto=id_producto)

        # Descuento en billetera
        cliente.billetera = billetera_Decimal - precio_total
        cliente.save(update_fields=['billetera'])

        # Descuento de stock
        producto.stock -= 1
        producto.save(update_fields=['stock'])

        # Registro de la compra (garantía = garantía extendida)
        ProductoModel.RegistroCompra.objects.create(
            cliente=cliente,
            producto=producto,
            precio_total=float(precio_total),
            garantia=garantia_extendida,   # True si compró extensión
            delivery=delivery
        )

        messages.success(
            request,
            f"¡Compra exitosa! Has adquirido '{producto.nombre}'. "
            f"Total pagado: ${precio_total}. Tu nuevo saldo es: ${cliente.billetera}"
        )

        return redirect('detalleProducto', id_producto=id_producto)

    # GET -> mostrar resumen antes de confirmar
    data = {
        'producto': producto,
        'cliente': cliente,
        'precio_base': precio_base,
        'precio_garantia': precio_garantia,
        'precio_delivery': precio_delivery,
        'precio_total_maximo': precio_base + precio_garantia + precio_delivery,
    }
    return render(request, 'Producto/confirmar_compra.html', data)


