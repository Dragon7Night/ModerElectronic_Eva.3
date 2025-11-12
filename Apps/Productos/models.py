from django.db import models
from django.conf import settings


# -MODELS -> PRODUCTOS 

""" NOTAS

. Las ID y PrimaryKey se crean automaticamente
. Los indices se crean de manera automatica cuando se referencian las ForeingKey


"""

# ~============= PRODUCTO / CATEGORIA =============~

# |===> CLASS Categoria [PK id_categoria]
class Categoria(models.Model):

    nombre = models.CharField(max_length=25)
    fecha_registro = models.DateTimeField(auto_now_add=True)


# |===> CLASS Producto [PK id_producto | FK admin_id]
class Producto(models.Model):

    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="prod_registrados")
    nombre = models.CharField(max_length=50)
    precio = models.FloatField()
    stock = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)


# |===> CLASS ProductoCategoria [PK id_produc_cate | FK producto_id, categoria_id]
class ProductoCategoria(models.Model):

    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)
    categoria_id = models.ForeignKey(Categoria, on_delete=models.CASCADE)


# ~============= VALORACIONES =============~

# |===> CLASS Comentario [PK id_comentario | FK cliente_id]
class Comentario(models.Model):

    realizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comentarios")
    comentario = models.CharField(max_length=300)
    fecha_registro = models.DateTimeField(auto_now_add=True)


# |===> CLASS ComentarioProducto [PK id_com_pro | FK comentario_id, producto_id]
class ComentarioProducto(models.Model):

    comentario_id = models.ForeignKey(Comentario, on_delete=models.CASCADE)
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)

# -----------------------------------------------------------

# |===> CLASS Calificacion [PK id_calificacion | FK cliente_id]
class Calificacion(models.Model):

    realizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="calificaciones")
    cant_estrella = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)


# |===> CLASS CalificacionProducto [PK id_cal_pro | FK calificacion_id, producto_id]
class CalificacionProducto(models.Model):

    calificacion_id = models.ForeignKey(Calificacion, on_delete=models.CASCADE)
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)


# ~============= SOLICITUDES =============~

# |===> CLASS Solicitud [PK id_solicitud | FK cliente_id, producto_id]
class Solicitud(models.Model):

    realizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="solicitudes")
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=300)
    estado = models.BooleanField()
    tipo_solicitud = models.CharField(max_length=20)
    fecha_registro = models.DateTimeField(auto_now_add=True)



# ~============= REGISTRO DE COMPRA =============~

# |===> CLASS RegistroCompra [PK id_registro_compra | FK cliente_id, producto_id]
class RegistroCompra(models.Model):

    cliente_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio_total = models.FloatField()
    garantia = models.BooleanField()
    delivery = models.BooleanField()
    fecha_compra = models.DateTimeField(auto_now_add=True)





