from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import Usuario, ClaveAcceso


class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('camposExtras', {'fields': ('nombre', 'direccion', 'rol', 'billetera')}),
    )
    list_display = ('username', 'email', 'nombre', 'rol', 'is_staff')

admin.site.register(Usuario, UsuarioAdmin)


class ClaveAccesoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_creacion')

admin.site.register(ClaveAcceso, ClaveAccesoAdmin)