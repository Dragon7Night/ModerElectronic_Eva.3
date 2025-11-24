from django.contrib import admin

from .models import Producto, Categoria, Comentario, Calificacion, Solicitud


class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id','nombre','precio','stock']

admin.site.register(Producto, ProductoAdmin)


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id','nombre']

admin.site.register(Categoria, CategoriaAdmin)


class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['id','comentario']

admin.site.register(Comentario, ComentarioAdmin)


class CalificacionAdmin(admin.ModelAdmin):
    list_display = ['id','cant_estrella']

admin.site.register(Calificacion, CalificacionAdmin)


class SolicitudAdmin(admin.ModelAdmin):
    list_display = ['id','descripcion','estado','tipo_solicitud']

admin.site.register(Solicitud, SolicitudAdmin)


