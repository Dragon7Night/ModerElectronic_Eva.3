
# '======[Importaciones]============================'
from django.urls import path
import Apps.Productos.views as productoViews
# '==============================================='

# °===========================°
#    °URLs -> Usuarios
# °===========================°

urlpatterns = [

    path('home/', productoViews.homeGeneral, name='homeGeneral' ),

    # ------------------------
    #   -URLs de Productos
    # ------------------------
    path('catalogo-producto/', productoViews.catalogo_producto, name='catalogoProductos'),
    path('producto/<int:id_producto>/', productoViews.detalle_producto, name='detalleProducto'),

    path('registrar-producto/', productoViews.registrar_producto, name='registrarProducto'),
    path('editar-producto/<int:id_producto>', productoViews.editar_producto, name='editarProducto'),
    path('eliminar-producto/<int:id_producto>', productoViews.eliminar_producto, name='eliminarProducto'),

    path('confirmar-compra/<int:id_producto>/',productoViews.confirmar_compra,name='confirmarCompra'),
    # path("comprar/<int:id_producto>/", productoViews.comprar_producto, name="comprarProducto"),

    # ------------------------
    #   -URLs de Categoria
    # ------------------------
    path('registrar-categoria/', productoViews.registrar_categoria, name='registrarCategoria'),
    
    # ------------------------
    #   -URLs de Calificación
    # ------------------------
    path('data-calificacion/', productoViews.data_categoria, name='dataCalificacion'),
    path('producto/calificacion/<int:id_producto>/', productoViews.agregar_calificacion, name='agregarCalificacion'),

    # ------------------------
    #   -URLs de Solicitud
    # ------------------------
    path('registrar-solicitud/<int:registro_id>/', productoViews.register_solicitud, name='registrarSolicitud'),
    path('data-solicitud/', productoViews.data_Solicitud, name='dataSolicitud'),
    
    path('solicitud/<int:solicitud_id>/aprobar/', productoViews.aprobar_solicitud, name='aprobarSolicitud'),
    path('solicitud/<int:solicitud_id>/rechazar/', productoViews.rechazar_solicitud, name='rechazarSolicitud'),

]

