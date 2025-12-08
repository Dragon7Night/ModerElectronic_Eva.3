from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
import random

from Apps.Usuarios.models import Usuario
from Apps.Productos.models import (
    Categoria,
    Producto,
    ProductoCategoria,
    Calificacion,
    Solicitud,
    RegistroCompra,
)

"""
Comando para ejecutar la generación masiva de datos de prueba

Ejemplos:
python manage.py generador_car --productos 2000

py .\manage.py generador_car --usuarios 10 --admins 10 --productos 1000 --calificaciones 1000 --solicitudes 100 --compras 1000

NOTAS:
- El parámetro --comentarios se mantiene solo por compatibilidad,
  pero ya no se usa porque comentario y estrellas están unificados en Calificacion.
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

# Listas para nombres "reales" de productos
MARCAS = [
    "Logitech", "Samsung", "Sony", "LG", "Asus", "HP", "Dell", "Lenovo",
    "Xiaomi", "Razer", "Corsair", "Kingston", "HyperX", "Huawei"
]

PLANTILLAS_PRODUCTO = [
    "Mouse inalámbrico {marca}",
    "Teclado mecánico {marca}",
    "Audífonos Bluetooth {marca}",
    "Altavoces estéreo {marca}",
    "Monitor LED 24\" {marca}",
    "Televisor Smart 50\" {marca}",
    "Notebook 14\" {marca}",
    "PC de escritorio gamer {marca}",
    "Impresora multifuncional {marca}",
    "Router inalámbrico {marca}",
    "Adaptador USB a HDMI {marca}",
    "Consola de videojuegos {marca}",
    "Barra de sonido {marca}",
    "Webcam Full HD {marca}",
]

def generar_nombre_producto():
    marca = random.choice(MARCAS)
    plantilla = random.choice(PLANTILLAS_PRODUCTO)
    return plantilla.format(marca=marca)


# Comentarios "coherentes" según la cantidad de estrellas
COMENTARIOS_5 = [
    "Excelente producto, superó totalmente mis expectativas.",
    "Funciona perfecto, la calidad es muy buena.",
    "Muy recomendable, volvería a comprarlo sin dudar.",
    "Entrega rápida y el producto llegó en perfectas condiciones.",
    "La relación calidad/precio es increíble.",
]

COMENTARIOS_4 = [
    "Muy buen producto, cumple con casi todo lo prometido.",
    "Funciona bien, aunque podría mejorar en algunos detalles.",
    "Me dejó conforme, es una buena compra.",
    "En general satisfecho, solo pequeños detalles.",
    "Buen rendimiento para el precio que tiene.",
]

COMENTARIOS_3 = [
    "Es aceptable, aunque me esperaba un poco más.",
    "Cumple, pero hay cosas que se podrían mejorar.",
    "No está mal, hace lo que promete sin destacar.",
    "Regular, ni muy bueno ni muy malo.",
    "Por el precio está bien, pero he visto mejores.",
]

COMENTARIOS_2 = [
    "No quedé del todo conforme con el producto.",
    "Funciona, pero tiene varios problemas de uso.",
    "La calidad es baja para el precio que pagué.",
    "Esperaba mucho más, no lo volvería a comprar.",
    "El rendimiento deja bastante que desear.",
]

COMENTARIOS_1 = [
    "Muy mala experiencia, el producto llegó con fallas.",
    "No funciona como debería, estoy decepcionado.",
    "La calidad es pésima, no lo recomiendo.",
    "Dejó de funcionar al poco tiempo de usarlo.",
    "No vale la pena, tiré el dinero a la basura.",
]


def generar_comentario(estrellas: int) -> str:
    if estrellas >= 5:
        lista = COMENTARIOS_5
    elif estrellas == 4:
        lista = COMENTARIOS_4
    elif estrellas == 3:
        lista = COMENTARIOS_3
    elif estrellas == 2:
        lista = COMENTARIOS_2
    else:
        lista = COMENTARIOS_1
    return random.choice(lista)


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
            help="(IGNORADO) Comentarios y calificaciones se generan juntos en Calificacion.",
        )
        parser.add_argument(
            "--calificaciones",
            type=int,
            default=1000,
            help="Cantidad de calificaciones (estrella + comentario) a crear.",
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
        cant_productos = options["productos"]
        cant_calificaciones = options["calificaciones"]
        cant_solicitudes = options["solicitudes"]
        cant_compras = options["compras"]

        self.stdout.write(self.style.MIGRATE_HEADING("== Generando datos de prueba =="))

        # 1) Crear admins
        self.stdout.write(self.style.NOTICE("Creando administradores..."))
        admins = []
        for i in range(cant_admins):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"admin_{first_name.lower()}_{last_name.lower()}_{i}"

            admin, created = Usuario.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": fake.unique.email(),
                    "direccion": fake.address()[:90],
                    "rol": Usuario.ROL_ADMIN,
                    "billetera": random.uniform(0, 500000),
                },
            )
            if created:
                admin.set_password("admin123")
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()
            admins.append(admin)

        if not admins:
            admins = list(Usuario.objects.filter(rol=Usuario.ROL_ADMIN))
        if not admins:
            raise RuntimeError("No hay administradores disponibles para asociar productos.")

        # 2) Crear clientes
        self.stdout.write(self.style.NOTICE("Creando clientes..."))
        clientes = []
        for i in range(cant_usuarios):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"cliente_{first_name.lower()}_{last_name.lower()}_{i}"

            cliente, created = Usuario.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": fake.unique.email(),
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

        # 4) Crear productos con nombres de dispositivos electrónicos
        self.stdout.write(self.style.NOTICE("Creando productos..."))
        productos = []
        for i in range(cant_productos):
            admin = random.choice(admins)
            producto = Producto(
                admin=admin,
                nombre=generar_nombre_producto(),
                precio=round(random.uniform(5000, 500000), 2),
                stock=random.randint(0, 500),
            )
            productos.append(producto)

        Producto.objects.bulk_create(productos, batch_size=1000)
        productos = list(Producto.objects.all())

        # 5) Relacionar productos con categorías (SOLO las fijas)
        self.stdout.write(self.style.NOTICE("Asignando categorías a productos..."))
        relaciones = []
        for producto in productos:
            num_cat = random.randint(1, min(3, len(categorias)))
            categorias_producto = random.sample(categorias, num_cat)
            for cat in categorias_producto:
                relaciones.append(
                    ProductoCategoria(producto_id=producto, categoria_id=cat)
                )
        ProductoCategoria.objects.bulk_create(relaciones, batch_size=1000)

        # 6) Crear calificaciones (estrella + comentario) respetando unique_together
        self.stdout.write(self.style.NOTICE("Creando calificaciones (con comentario)..."))

        existing_pairs = set(
            Calificacion.objects.values_list("producto_id", "cliente_id")
        )

        max_pairs_posibles = len(productos) * len(clientes)
        espacio_disponible = max_pairs_posibles - len(existing_pairs)
        if espacio_disponible <= 0:
            self.stdout.write(
                self.style.WARNING(
                    "No hay combinaciones (producto, cliente) libres para crear nuevas calificaciones."
                )
            )
            objetivo = 0
        else:
            objetivo = min(cant_calificaciones, espacio_disponible)

        calificaciones = []
        intentos = 0
        max_intentos = objetivo * 5 if objetivo > 0 else 0

        while len(calificaciones) < objetivo and intentos < max_intentos:
            intentos += 1
            producto = random.choice(productos)
            cliente = random.choice(clientes)
            pair = (producto.id, cliente.id)

            if pair in existing_pairs:
                continue

            existing_pairs.add(pair)

            estrellas = random.randint(1, 5)
            comentario_texto = generar_comentario(estrellas)

            calificaciones.append(
                Calificacion(
                    producto=producto,
                    cliente=cliente,
                    cant_estrella=estrellas,
                    comentario=comentario_texto,
                )
            )

        if calificaciones:
            Calificacion.objects.bulk_create(calificaciones, batch_size=1000)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Se crearon {len(calificaciones)} calificaciones nuevas."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING("No se crearon nuevas calificaciones.")
            )

        # 7) Crear solicitudes
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

        # 8) Crear registros de compra
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
