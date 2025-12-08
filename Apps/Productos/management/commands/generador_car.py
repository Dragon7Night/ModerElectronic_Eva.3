from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
import random

from Apps.Usuarios.models import Usuario
from Apps.Productos.models import (
    Categoria,
    Producto,
    ProductoCategoria,
    Comentario,
    Calificacion,
    Solicitud,
    RegistroCompra,
)


""" 
Comando para ejecutar la generación masiva de datos de prueba

Ejemplo
python manage.py generador_car --productos 2000

py .\manage.py generador_car --usuarios 10 --admins 10 --productos 1000 --comentarios 1000 --calificaciones 1000 --solicitudes 100 --compras 1000
"""

# Lista fija de categorías permitidas
CATEGORIAS_FIJAS = [
    "adaptadores",
    "altavoces",
    "audifonos",
    "computadoras",
    "consolas",
    "impresoras",
    "inalambricos",
    "mouse",
    "televisores",
    "teclados",
    "otros",
]


class Command(BaseCommand):
    help = "Genera datos de prueba masivos para pruebas de rendimiento."

    def add_arguments(self, parser):
        parser.add_argument(
            "--usuarios",
            type=int,
            default=50,
            help="Cantidad de usuarios clientes a crear (además de admins).",
        )
        parser.add_argument(
            "--admins",
            type=int,
            default=5,
            help="Cantidad de usuarios administradores a crear.",
        )
        parser.add_argument(
            "--categorias",
            type=int,
            default=10,
            help="(Ignorado) Cantidad de categorías a crear. Ahora se usan categorías fijas.",
        )
        parser.add_argument(
            "--productos",
            type=int,
            default=500,
            help="Cantidad de productos a crear.",
        )
        parser.add_argument(
            "--comentarios",
            type=int,
            default=1000,
            help="Cantidad de comentarios a crear.",
        )
        parser.add_argument(
            "--calificaciones",
            type=int,
            default=1000,
            help="Cantidad de calificaciones a crear.",
        )
        parser.add_argument(
            "--solicitudes",
            type=int,
            default=300,
            help="Cantidad de solicitudes a crear.",
        )
        parser.add_argument(
            "--compras",
            type=int,
            default=800,
            help="Cantidad de registros de compra a crear.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        fake = Faker("es_CL")

        cant_usuarios = options["usuarios"]
        cant_admins = options["admins"]
        # cant_categorias = options["categorias"]  # ahora no se usa para crear, solo dejamos el argumento por compatibilidad
        cant_productos = options["productos"]
        cant_comentarios = options["comentarios"]
        cant_calificaciones = options["calificaciones"]
        cant_solicitudes = options["solicitudes"]
        cant_compras = options["compras"]

        self.stdout.write(self.style.MIGRATE_HEADING("== Generando datos de prueba =="))

        # 1) Crear admins
        self.stdout.write(self.style.NOTICE("Creando administradores..."))
        admins = []
        for i in range(cant_admins):
            username = f"admin_demo_{i}"
            admin, _ = Usuario.objects.get_or_create(
                username=username,
                defaults={
                    "email": fake.email(),
                    "direccion": fake.address()[:90],
                    "rol": Usuario.ROL_ADMIN,
                    "billetera": random.uniform(0, 500000),
                },
            )
            # Si es nuevo, asignamos contraseña
            admin.set_password("admin123")
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()
            admins.append(admin)

        if not admins:
            # fallback por si no se creó ninguno (muy raro)
            admins = list(Usuario.objects.filter(rol=Usuario.ROL_ADMIN))
        if not admins:
            raise RuntimeError("No hay administradores disponibles para asociar productos.")

        # 2) Crear clientes
        self.stdout.write(self.style.NOTICE("Creando clientes..."))
        clientes = []
        for i in range(cant_usuarios):
            username = f"cliente_demo_{i}"
            cliente, created = Usuario.objects.get_or_create(
                username=username,
                defaults={
                    "email": fake.email(),
                    "direccion": fake.address()[:90],
                    "rol": Usuario.ROL_CLIENTE,
                    "billetera": random.uniform(0, 300000),
                },
            )
            if created:
                cliente.set_password("cliente123")
                cliente.save()
            clientes.append(cliente)

        if not clientes:
            clientes = list(Usuario.objects.filter(rol=Usuario.ROL_CLIENTE))
        if not clientes:
            raise RuntimeError("No hay clientes disponibles para asociar datos.")

        # 3) Crear categorías FIJAS
        self.stdout.write(self.style.NOTICE("Creando categorías fijas..."))
        categorias = []
        for nombre in CATEGORIAS_FIJAS:
            categoria, _ = Categoria.objects.get_or_create(nombre=nombre)
            categorias.append(categoria)

        self.stdout.write(
            self.style.SUCCESS(
                f"Se usarán {len(categorias)} categorías fijas: {', '.join(CATEGORIAS_FIJAS)}"
            )
        )

        # 4) Crear productos
        self.stdout.write(self.style.NOTICE("Creando productos..."))
        productos = []
        for i in range(cant_productos):
            admin = random.choice(admins)
            producto = Producto(
                admin=admin,
                nombre=fake.sentence(nb_words=3)[:100],
                precio=round(random.uniform(1000, 500000), 2),
                stock=random.randint(0, 500),
            )
            productos.append(producto)

        Producto.objects.bulk_create(productos, batch_size=1000)
        productos = list(Producto.objects.all())

        # 5) Relacionar productos con categorías (SOLO las fijas)
        self.stdout.write(self.style.NOTICE("Asignando categorías a productos..."))
        relaciones = []
        for producto in productos:
            # de 1 a 3 categorías por producto, pero siempre dentro de CATEGORIAS_FIJAS
            num_cat = random.randint(1, min(3, len(categorias)))
            categorias_producto = random.sample(categorias, num_cat)
            for cat in categorias_producto:
                relaciones.append(
                    ProductoCategoria(producto_id=producto, categoria_id=cat)
                )
        ProductoCategoria.objects.bulk_create(relaciones, batch_size=1000)

        # 6) Crear comentarios
        self.stdout.write(self.style.NOTICE("Creando comentarios..."))
        comentarios = []
        for i in range(cant_comentarios):
            producto = random.choice(productos)
            cliente = random.choice(clientes)
            comentarios.append(
                Comentario(
                    producto=producto,
                    cliente=cliente,
                    comentario=fake.text(max_nb_chars=200),
                )
            )
        Comentario.objects.bulk_create(comentarios, batch_size=1000)

        # 7) Crear calificaciones
        self.stdout.write(self.style.NOTICE("Creando calificaciones..."))
        calificaciones = []
        for i in range(cant_calificaciones):
            producto = random.choice(productos)
            cliente = random.choice(clientes)
            estrella = random.randint(1, 5)
            calificaciones.append(
                Calificacion(
                    producto=producto,
                    cliente=cliente,
                    cant_estrella=estrella,
                )
            )
        Calificacion.objects.bulk_create(calificaciones, batch_size=1000)

        # 8) Crear solicitudes
        self.stdout.write(self.style.NOTICE("Creando solicitudes..."))
        solicitudes = []
        tipos = ["en revision", "aprobada", "rechazada"]
        for i in range(cant_solicitudes):
            producto = random.choice(productos)
            cliente = random.choice(clientes)
            solicitudes.append(
                Solicitud(
                    cliente=cliente,
                    producto=producto,
                    descripcion=fake.text(max_nb_chars=200),
                    estado=random.choice([True, False]),
                    tipo_solicitud=random.choice(tipos),
                )
            )
        Solicitud.objects.bulk_create(solicitudes, batch_size=1000)

        # 9) Crear registros de compra
        self.stdout.write(self.style.NOTICE("Creando registros de compra..."))
        compras = []
        for i in range(cant_compras):
            producto = random.choice(productos)
            cliente = random.choice(clientes)
            precio_total = producto.precio * random.randint(1, 3)
            compras.append(
                RegistroCompra(
                    cliente=cliente,
                    producto=producto,
                    precio_total=precio_total,
                    garantia=random.choice([True, False]),
                    delivery=random.choice([True, False]),
                )
            )
        RegistroCompra.objects.bulk_create(compras, batch_size=1000)

        self.stdout.write(self.style.SUCCESS("✅ Datos de prueba generados correctamente."))
        self.stdout.write(self.style.SUCCESS("  - Admins:       %s" % len(admins)))
        self.stdout.write(self.style.SUCCESS("  - Clientes:     %s" % len(clientes)))
        self.stdout.write(self.style.SUCCESS("  - Categorías:   %s" % len(categorias)))
        self.stdout.write(self.style.SUCCESS("  - Productos:    %s" % len(productos)))
