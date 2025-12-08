# Apps/Productos/models.py

# '======[Importaciones]============================'
from django.db import models

from Apps.Usuarios import models as UsuarioModel  # model de usuarios de Django
from django.conf import settings
# '================================================='

# °===========================°
#    °Modelos -> Productos
# °===========================°

""" NOTAS
. Las ID y PrimaryKey se crean automaticamente
. Los indices se crean de manera automatica cuando se referencian las ForeingKey
"""

# ~============= PRODUCTO / CATEGORIA =============~

class Categoria(models.Model):

    nombre = models.CharField(max_length=50, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):

    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='productos_administrados'
    )
    
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()
    stock = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class ProductoCategoria(models.Model):

    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)
    categoria_id = models.ForeignKey(Categoria, on_delete=models.CASCADE)


# ~============= VALORACIONES (UNIFICADO) =============~

class Calificacion(models.Model):

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='calificaciones'
    )
    cliente = models.ForeignKey(
        UsuarioModel.Usuario,
        on_delete=models.CASCADE
    )

    # 1 a 5 estrellas
    cant_estrella = models.IntegerField()
    # Comentario opcional
    comentario = models.CharField(max_length=300, blank=True)

    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('producto', 'cliente')

    def __str__(self):
        return f"{self.cant_estrella} estrellas - {self.producto.nombre}"


# ~============= REGISTRO DE COMPRA =============~

class RegistroCompra(models.Model):

    cliente = models.ForeignKey(
        UsuarioModel.Usuario,
        on_delete=models.CASCADE
    )
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio_total = models.FloatField()
    garantia = models.BooleanField(default=False)
    delivery = models.BooleanField(default=False)
    fecha_compra = models.DateTimeField(auto_now_add=True)


# ~============= SOLICITUDES =============~

class Solicitud(models.Model):

    cliente = models.ForeignKey(UsuarioModel.Usuario, on_delete=models.CASCADE) 
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    registro_compra = models.ForeignKey(
        RegistroCompra,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    descripcion = models.CharField(max_length=300)
    estado = models.BooleanField(default=True)
    tipo_solicitud = models.CharField(max_length=20, default='en revision')
    fecha_registro = models.DateTimeField(auto_now_add=True)
