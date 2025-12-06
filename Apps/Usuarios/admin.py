
# '======[Importaciones]============================'
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Apps.Usuarios import models as ModelUsuarios
# '================================================='

# °===========================°
#    °Admin CRUD -> Usuarios
# °===========================°

# -.-.-.-.-.- CRUD de Usuarios -.-.-.-.-.-
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('camposExtras', {'fields': ('direccion', 'rol', 'billetera')}),
    )
    list_display = ['username', 'email', 'rol', 'is_staff']

admin.site.register(ModelUsuarios.Usuario, UsuarioAdmin)


