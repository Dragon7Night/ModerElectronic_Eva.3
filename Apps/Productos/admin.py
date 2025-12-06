
# '======[Importaciones]============================'
from django.contrib import admin

from Apps.Productos import models as ModelProductos
# '================================================='

# °=============================°
#    °Admin CRUD -> Productos
# °=============================°

# -.-.-.-.-.- CRUD de Productos -.-.-.-.-.-
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id','nombre','precio','stock']

admin.site.register(ModelProductos.Producto, ProductoAdmin)


# -.-.-.-.-.- CRUD de Categorias -.-.-.-.-.-
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id','nombre']

admin.site.register(ModelProductos.Categoria, CategoriaAdmin)


# -.-.-.-.-.- CRUD de Comentarios -.-.-.-.-.-
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['id','comentario']

admin.site.register(ModelProductos.Comentario, ComentarioAdmin)


# -.-.-.-.-.- CRUD de Calificaciones -.-.-.-.-.-
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ['id','cant_estrella']

admin.site.register(ModelProductos.Calificacion, CalificacionAdmin)


# -.-.-.-.-.- CRUD de Solicitudes -.-.-.-.-.-
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ['id','descripcion','estado','tipo_solicitud']

admin.site.register(ModelProductos.Solicitud, SolicitudAdmin)

