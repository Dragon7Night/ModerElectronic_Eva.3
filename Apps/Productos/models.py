
# '======[Importaciones]============================'
from django.db import models

from Apps.Usuarios import models as UsuarioModel  # model de usuarios de Django

from django.conf import settings
# '================================================='

# °===========================°
#    °Vistas -> Productos
# °===========================°

""" NOTAS
. Las ID y PrimaryKey se crean automaticamente
. Los indices se crean de manera automatica cuando se referencian las ForeingKey
"""

# ~============= PRODUCTO / CATEGORIA =============~

# |===> CLASS Categoria [PK id_categoria]
class Categoria(models.Model):

    nombre = models.CharField(max_length=50, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

# |===> CLASS Producto [PK id_producto | FK admin_id]
class Producto(models.Model):

    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True,blank=True, related_name='productos_administrados')
    
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()
    stock = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.nombre

# |===> CLASS ProductoCategoria [PK id_produc_cate | FK producto_id, categoria_id]
class ProductoCategoria(models.Model):

    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)
    categoria_id = models.ForeignKey(Categoria, on_delete=models.CASCADE)


# ~============= VALORACIONES =============~

# |===> CLASS Comentario [PK id_comentario | FK cliente_id]

class Comentario(models.Model):

    # producto_id
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='comentarios')
    # cliente_id
    cliente = models.ForeignKey(UsuarioModel.Usuario, on_delete=models.CASCADE)
    comentario = models.CharField(max_length=300)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.producto.nombre}"

# -----------------------------------------------------------

# |===> CLASS Calificacion [PK id_calificacion | FK cliente_id]
class Calificacion(models.Model):

    # producto_id
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='calificaciones')
    # cliente_id
    cliente = models.ForeignKey(UsuarioModel.Usuario, on_delete=models.CASCADE)
    cant_estrella = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cant_estrella} estrellas - {self.producto.nombre}"

# ~============= SOLICITUDES =============~

# |===> CLASS Solicitud [PK id_solicitud | FK cliente_id, producto_id]
class Solicitud(models.Model):

    # cliente_id
    cliente = models.ForeignKey(UsuarioModel.Usuario, on_delete=models.CASCADE) 
    # producto_id
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=300)
    estado = models.BooleanField(default=True)
    tipo_solicitud = models.CharField(max_length=20, default='en revision')
    fecha_registro = models.DateTimeField(auto_now_add=True)



# ~============= REGISTRO DE COMPRA =============~

# |===> CLASS RegistroCompra [PK id_registro_compra | FK cliente_id, producto_id]

class RegistroCompra(models.Model):

    # cliente_id
    cliente = models.ForeignKey(UsuarioModel.Usuario, on_delete=models.CASCADE) # Vinculado al usuario
    # producto_id
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio_total = models.FloatField()
    garantia = models.BooleanField(default=False)
    delivery = models.BooleanField(default=False)
    fecha_compra = models.DateTimeField(auto_now_add=True)

