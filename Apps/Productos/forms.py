from django import forms
from .models import Producto, Comentario, Calificacion,Categoria

from django.core import validators

# -FORMS -> PRODUCTOS 

# ~============= PRODUCTO / CATEGORIA =============~

# |===> CLASS Categoria [PK id_categoria]
class Categoria(forms.Form):

    nombre = forms.CharField(validators=[
        validators.MinLengthValidator(3),
        validators.MaxLengthValidator(25)
    ])

    nombre.label = 'Nombre'
    
    nombre.widget.attrs['class'] = 'form-control'

# |===> CLASS Producto [PK id_producto | FK admin_id]
class Producto(forms.Form):

    nombre = forms.CharField(validators=[
        validators.MinLengthValidator(3),
        validators.MaxLengthValidator(25)
    ])
    precio = forms.FloatField(validators=[
        validators.MinValueValidator(0)
    ])
    stock = forms.IntegerField()

    nombre.label = 'Nombre'
    precio.label = 'Precio'
    stock.label = 'stock'

    nombre.widget.attrs['class'] = 'form-control'
    precio.widget.attrs['class'] = 'form-control'
    stock.widget.attrs['class'] = 'form-control'


# ~============= VALORACIONES =============~

# |===> CLASS Comentario [PK id_comentario | FK cliente_id]
class Comentario(forms.Form):

    comentario = forms.CharField(validators=[
        validators.MinLengthValidator(3),
        validators.MaxLengthValidator(25)
    ])

    comentario.label = 'Comentario'

    comentario.widget.attrs['class'] = 'form-control'

# -----------------------------------------------------------

# |===> CLASS Calificacion [PK id_calificacion | FK cliente_id]
class Calificacion(forms.Form):

    cant_estrella = forms.IntegerField()

    cant_estrella.label = 'Cantidad de Estrellas'

    cant_estrella.widget.attrs['class'] = 'form-control'


# ~============= SOLICITUDES =============~

# |===> CLASS Solicitud [PK id_solicitud | FK cliente_id, producto_id]
class Solicitud(forms.Form):


    descripcion = forms.CharField(validators=[
        validators.MinLengthValidator(0),
        validators.MaxLengthValidator(300)
    ])
    
    descripcion.label = 'Nombre'

    descripcion.widget.attrs['class'] = 'form-control'


    # estado con EN PROCESO, APROBADO, DENEGADO
    # estado = forms.BooleanField()

    # LISTA DE OPCIONES LIMITADA, DEVOLUCION, GARANTIA
    # tipo_solicitud = forms.CharField(max_length=20)


