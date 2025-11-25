
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
    path('registrar-producto/', productoViews.registrar_producto, name='registrarProducto'),
    path('editar-producto/<int:id_producto>', productoViews.editar_producto, name='editarProducto'),
    path('eliminar-producto/<int:id_producto>', productoViews.eliminar_producto, name='eliminarProducto'),

    # ------------------------
    #   -URLs de Categoria
    # ------------------------
    path('registrar-categoria/', productoViews.registrar_categoria, name='registrarCategoria'),
    
    # ------------------------
    #   -URLs de Calificación
    # ------------------------
    path('agregar-calificacion/<int:id_producto>', productoViews.agregar_Calificacion, name='registrarCalificacion'),
    path('data-calificacion/', productoViews.data_categoria, name='dataCalificacion'),

    # ------------------------
    #   -URLs de Solicitud
    # ------------------------
    # path('registrar-solicitud/<int:id_producto>', productoViews.register_Solicitud, name='registrarSolicitud'),
    path('data-solicitud/', productoViews.data_Solicitud, name='dataSolicitud'),

        # NUEVA RUTA DETALLE
    path('producto/<int:id_producto>/', productoViews.detalle_producto, name='detalleProducto'),
    
    # RUTA PARA PROCESAR EL COMENTARIO (POST)
    path('producto/feedback/<int:id_producto>/', productoViews.agregar_feedback, name='agregarFeedback'),
]

