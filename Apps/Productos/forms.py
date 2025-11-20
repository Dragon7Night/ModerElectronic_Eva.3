
from django import forms
from Apps.Productos.models import *

from django.core import validators

# -FORMS -> PRODUCTOS

# ~============= PRODUCTO / CATEGORIA =============~

# |===> Formulario de EDICION <Categoria>
class RegisterCategoriaForm(forms.Form):

    # Definicion + validacion de campos
    nombre = forms.CharField(validators=[
        validators.MinLengthValidator(3),
        validators.MaxLengthValidator(25)
    ])

    # Tags personalizado para los campos
    nombre.label = 'Nombre de la categoria'

    # Style para formulario - BS5
    nombre.widget.attrs['class'] = 'form-control'

# ._____________________

# |===> Formulario de CREACION <Categoria>
class RegisterCategoriaForm(forms.ModelForm):

    # Modelo de registro del formulario
    class Meta:
        model = Categoria
        fields = '__all__'
    
    # Definicion + validacion de campos
    nombre = forms.CharField(validators=[
        validators.MinLengthValidator(3),
        validators.MaxLengthValidator(25)])

# |<><><><><><><><><><><><><><><><><><><><><><><><>|

# |===> Formulario de EDICION <Producto>
class RegisterProductoForm(forms.Form):

    # Definicion + validacion de campos
    nombre = forms.CharField(validators=[
        validators.MinLengthValidator(3),
        validators.MaxLengthValidator(25)
    ])
    precio = forms.FloatField(validators=[
        validators.MinValueValidator(0)
    ])
    stock = forms.IntegerField(validators=[
        validators.MinValueValidator(0)
    ])
    
    # Tags personalizado para los campos
    nombre.label = 'Nombre del producto'
    precio.label = 'Precio'
    stock.label = 'Stock'

    # Style para formulario - BS5
    nombre.widget.attrs['class'] = 'form-control'
    precio.widget.attrs['class'] = 'form-control'
    stock.widget.attrs['class'] = 'form-control'

# ._____________________

# |===> Formulario de CREACION <Producto>
class RegisterProductoForm(forms.ModelForm):

    # Modelo de registro del formulario
    class Meta:
        model = Producto
        fields = '__all__'
    
    # Definicion + validacion de campos
    nombre = forms.CharField(validators=[
        validators.MinLengthValidator(3),
        validators.MaxLengthValidator(25)
    ])
    precio = forms.FloatField(validators=[
        validators.MinValueValidator(0)
    ])
    stock = forms.IntegerField(validators=[
        validators.MinValueValidator(0)
    ])


# ~============= VALORACIONES =============~

# |===> Formulario de EDICION <Comentarios>
class RegisterComentarioForm(forms.Form):

    # Definicion + validacion de campos
    comentario = forms.CharField(validators=[
        validators.MinLengthValidator(3),
        validators.MaxLengthValidator(300)
    ])
    
    # Tags personalizado para los campos
    comentario.label = 'Comentario'

    # Style para formulario - BS5
    comentario.widget.attrs['class'] = 'form-control'

# ._____________________

# |===> Formulario de CREACION <Comentarios>
class RegisterComentarioForm(forms.ModelForm):
    
    # Modelo de registro del formulario
    class Meta:
        model = Comentario
        fields = '__all__'
    
    # Definicion + validacion de campos
    comentario = forms.CharField(validators=[
        validators.MinLengthValidator(3),
        validators.MaxLengthValidator(50)])
    
# |<><><><><><><><><><><><><><><><><><><><><><><><>|

# |===> Formulario de EDICION <Calificacion>
class RegisterCalificacionForm(forms.Form):

    # Definicion + validacion de campos
    cant_estrella = forms.IntegerField(validators=[
        validators.MinValueValidator(0),
        validators.MaxValueValidator(5)
    ])
   
    # Tags personalizado para los campos
    cant_estrella.label = 'Cantidad de Estrellas'

    # Style para formulario - BS5
    cant_estrella.widget.attrs['class'] = 'form-control'

# ._____________________

# |===> Formulario de CREACION <Calificacion>
class RegisterCalificacionForm(forms.ModelForm):
    
    # Modelo de registro del formulario
    class Meta:
        model = Calificacion
        fields = '__all__'

    # Definicion + validacion de campos  
    cant_estrella = forms.IntegerField(validators=[
        validators.MinValueValidator(0),
        validators.MaxValueValidator(5)
    ])

# ~============= SOLICITUDES =============~

# |===> Formulario de EDICION <Solicitudes>
class RegisterSolicitudForm(forms.Form):

    # Definicion + validacion de campos
    descripcion = forms.CharField(validators=[
        validators.MinLengthValidator(0),
        validators.MaxLengthValidator(300)
    ])
    estado = forms.BooleanField()
    tipo_solicitud = forms.CharField()
    
    # Tags personalizado para los campos
    descripcion.label = 'Descripcion del producto'
    estado.label = 'Estado'
    tipo_solicitud.label = 'Tipo de Solicitud'

    # Style para formulario - BS5
    descripcion.widget.attrs['class'] = 'form-control'
    estado.widget.attrs['class'] = 'form-control'
    tipo_solicitud.widget.attrs['class'] = 'form-control'

# ._____________________

# |===> Formulario de CREACION <Solicitud>
class RegisterSolicitudForm(forms.ModelForm):

    # Modelo de registro del formulario
    class Meta:
        model = Solicitud
        fields = ['descripcion']
    
    # Definicion + validacion de campos
    descripcion = forms.CharField(validators=[
        validators.MinLengthValidator(0),
        validators.MaxLengthValidator(300)])
   
    

# ~============= REGISTRO DE COMPRA =============~

#ACA NO EH TOCADO ABSOLUTAMENTE NADA AUN

# |===> CLASS RegistroCompra EDITAR [PK id_registro_compra | FK cliente_id, producto_id]
class RegistroCompra(forms.Form):

    # FK cliente
    # producto_id = forms.ForeignKey(validators=[
    #     validators.MinLengthValidator(3),
    #     validators.MaxLengthValidator(25)
    # ])
    precio_total = forms.FloatField()
    garantia = forms.BooleanField()
    delivery = forms.BooleanField()
    # fecha_compra = forms.DateTimeField(validators=[
    #     validators.MinLengthValidator(3),
    #     validators.MaxLengthValidator(25)
    # ])

# |===> style formulario de BS5 RegistroCompra

    precio_total.widget.attrs['class'] = 'form-control'
    garantia.widget.attrs['class'] = 'form-control'
    delivery.widget.attrs['class'] = 'form-control'
    # fecha_compra.widget.attrs['class'] = 'form-control'
    
    # Tag para RegistroCompra personalizado
    precio_total.label = 'Precio total'
    garantia.label = 'Garantia'
    delivery.label = 'Delivery'

    class RegistroCompra(forms.ModelForm):
        class Meta:
            model = Producto
            fields = '__all__'
        
        precio_total = forms.FloatField()
        garantia = forms.BooleanField()
        delivery = forms.BooleanField()





# CODE ANTERIOR 


# from django import forms
# from .models import Producto, Comentario, Calificacion,Categoria

# from django.core import validators

# # -FORMS -> PRODUCTOS 

# # ~============= PRODUCTO / CATEGORIA =============~

# # |===> CLASS Categoria [PK id_categoria]
# class Categoria(forms.Form):

#     nombre = forms.CharField(validators=[
#         validators.MinLengthValidator(3),
#         validators.MaxLengthValidator(25)
#     ])

#     nombre.label = 'Nombre'
    
#     nombre.widget.attrs['class'] = 'form-control'

# # |===> CLASS Producto [PK id_producto | FK admin_id]
# class Producto(forms.Form):

#     nombre = forms.CharField(validators=[
#         validators.MinLengthValidator(3),
#         validators.MaxLengthValidator(25)
#     ])
#     precio = forms.FloatField(validators=[
#         validators.MinValueValidator(0)
#     ])
#     stock = forms.IntegerField()

#     nombre.label = 'Nombre'
#     precio.label = 'Precio'
#     stock.label = 'stock'

#     nombre.widget.attrs['class'] = 'form-control'
#     precio.widget.attrs['class'] = 'form-control'
#     stock.widget.attrs['class'] = 'form-control'


# # ~============= VALORACIONES =============~

# # |===> CLASS Comentario [PK id_comentario | FK cliente_id]
# class Comentario(forms.Form):

#     comentario = forms.CharField(validators=[
#         validators.MinLengthValidator(3),
#         validators.MaxLengthValidator(25)
#     ])

#     comentario.label = 'Comentario'

#     comentario.widget.attrs['class'] = 'form-control'

# # -----------------------------------------------------------

# # |===> CLASS Calificacion [PK id_calificacion | FK cliente_id]
# class Calificacion(forms.Form):

#     cant_estrella = forms.IntegerField()

#     cant_estrella.label = 'Cantidad de Estrellas'

#     cant_estrella.widget.attrs['class'] = 'form-control'


# # ~============= SOLICITUDES =============~

# # |===> CLASS Solicitud [PK id_solicitud | FK cliente_id, producto_id]
# class Solicitud(forms.Form):


#     descripcion = forms.CharField(validators=[
#         validators.MinLengthValidator(0),
#         validators.MaxLengthValidator(300)
#     ])
    
#     descripcion.label = 'Nombre'

#     descripcion.widget.attrs['class'] = 'form-control'


#     # estado con EN PROCESO, APROBADO, DENEGADO
#     # estado = forms.BooleanField()

#     # LISTA DE OPCIONES LIMITADA, DEVOLUCION, GARANTIA
#     # tipo_solicitud = forms.CharField(max_length=20)


