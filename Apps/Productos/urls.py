
from django.urls import path
import Apps.Productos.views as productoViews

urlpatterns = [

    path('home/', productoViews.homeGeneral, name='homeGeneral' ),

    # -----------------------
    # URLs de Productos
    # -----------------------
    path('catalogo-productos/', productoViews.data_Producto, name='catalogoProductos'),
    path('registrar-producto/', productoViews.register_Producto, name='registrarProducto'),
    path('editar-producto/<int:id_producto>', productoViews.editar_producto, name='editarProducto'),
    path('eliminar-producto/<int:id_producto>', productoViews.eliminar_producto, name='eliminarProducto'),
    
    # -----------------------
    # URLs de Calificación
    # -----------------------
    path('agregar-calificacion/<int:id_producto>', productoViews.agregar_Calificacion, name='registrarCalificacion'),
    path('data-calificacion/', productoViews.data_Calificacion, name='dataCalificacion'),

    # -----------------------
    # URLs de Solicitud
    # -----------------------
    path('registrar-solicitud/<int:id_producto>', productoViews.register_Solicitud, name='registrarSolicitud'),
    path('data-solicitud/', productoViews.data_Solicitud, name='dataSolicitud'),

]