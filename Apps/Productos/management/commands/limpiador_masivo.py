from django.core.management.base import BaseCommand
from Apps.Productos.models import (
    Categoria,
    Producto,
    ProductoCategoria,
    Comentario,
    Calificacion,
    Solicitud,
    RegistroCompra,
)

from Apps.Usuarios.models import Usuario

# Comando para ejecutar la limpieza masiva de la DB
# python manage.py limpiar_masivo



class Command(BaseCommand):
    help = "Elimina datos de prueba generados para rendimiento (USAR SOLO EN ENTORNO DE PRUEBAS)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("⚠ Eliminando datos de prueba..."))

        # Productos y relaciones
        Comentario.objects.all().delete()
        Calificacion.objects.all().delete()
        Solicitud.objects.all().delete()
        RegistroCompra.objects.all().delete()
        ProductoCategoria.objects.all().delete()
        Producto.objects.all().delete()
        Categoria.objects.all().delete()

        # Usuarios demo (por nombre)
        Usuario.objects.filter(username__startswith="admin_demo_").delete()
        Usuario.objects.filter(username__startswith="cliente_demo_").delete()

        self.stdout.write(self.style.SUCCESS("✅ Datos demo eliminados."))
