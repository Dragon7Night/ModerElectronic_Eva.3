
# '======[Importaciones]============================'
from django import forms
from Apps.Productos import models as ProductoModel

from django.core import validators
# '================================================='

# °===========================°
#    °Formulario -> Productos
# °===========================°

# ~============= PRODUCTO / CATEGORIA =============~

# |===> Formulario de  CREACION y EDICION <Categoria>
class RegisterCategoriaForm(forms.ModelForm):

    # Modelo de registro del formulario
    class Meta:
        model = ProductoModel.Categoria
        fields = ['nombre']
        # fields = '__all__'
    
    # Definicion + validacion + style + label de campos
    nombre = forms.CharField(validators=[
        validators.MinLengthValidator(3),
        validators.MaxLengthValidator(25)],
        widget=forms.TextInput(attrs={'class':'form-control'}),
        label='Nombre de categoria'
        )

# |<><><><><><><><><><><><><><><><><><><><><><><><>|

# |===> Formulario de  CREACION y EDICION <Producto>
class RegisterProductoForm(forms.ModelForm):

    # Definicion + validacion + style + label de campos
    categoria_id = forms.ModelMultipleChoiceField(
        queryset=ProductoModel.Categoria.objects.all().order_by('nombre'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label='Asignar Categoría(s)'
        )
    
    # Modelo de registro del formulario
    class Meta:
        model = ProductoModel.Producto
        # fields = '__all__'
        fields = ['nombre','precio','stock']

    nombre = forms.CharField(validators=[
        validators.MinLengthValidator(3),
        validators.MaxLengthValidator(25)],
        widget=forms.TextInput(attrs={'class':'form-control'}),
        label='Nombre de producto'
        )
    precio = forms.FloatField(validators=[
        validators.MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'class':'form-control'}),
        label='Precio'
        )
    stock = forms.IntegerField(validators=[
        validators.MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'class':'form-control'}),
        label='Stock del producto'
        )


# ~============= VALORACIONES =============~

# |===> Formulario de CREACION y EDICION <Comentarios>
class RegisterComentarioForm(forms.ModelForm):

    # Modelo de registro del formulario
    class Meta:
        model = ProductoModel.Comentario
        fields = '__all__'

    # Definicion + validacion + style + label de campos
    comentario = forms.CharField(validators=[
        validators.MinLengthValidator(3),
        validators.MaxLengthValidator(300)],
        widget=forms.TextInput(attrs={'class':'form-control'}),
        label='Comentario del producto'
    )
    
# |<><><><><><><><><><><><><><><><><><><><><><><><>|

# |===> Formulario de CREACION y EDICION <Calificacion>
class RegisterCalificacionForm(forms.ModelForm):

    # Modelo de registro del formulario
    class Meta:
        model = ProductoModel.Calificacion
        fields = {'cant_estrella'}
        # fields = '__all__'

    # Definicion + validacion + style + label de campos
    cant_estrella = forms.IntegerField(validators=[
        validators.MinValueValidator(0),
        validators.MaxValueValidator(5)],
        widget=forms.NumberInput(attrs={'class':'form-control'}),
        label='Cantidad de estrellas'
    )

# ~============= SOLICITUDES =============~

# |===> Formulario de EDICION <Solicitudes>
# class RegisterSolicitudForm(forms.Form):

#     # Definicion + validacion de campos
#     descripcion = forms.CharField(validators=[
#         validators.MinLengthValidator(0),
#         validators.MaxLengthValidator(300)
#     ])
#     estado = forms.BooleanField()
#     tipo_solicitud = forms.CharField()
    
#     # Tags personalizado para los campos
#     descripcion.label = 'Descripcion del producto'
#     estado.label = 'Estado'
#     tipo_solicitud.label = 'Tipo de Solicitud'

#     # Style para formulario - BS5
#     descripcion.widget.attrs['class'] = 'form-control'
#     estado.widget.attrs['class'] = 'form-control'
#     tipo_solicitud.widget.attrs['class'] = 'form-control'

# ._____________________

# |===> Formulario de CREACION <Solicitud>
class RegisterSolicitudForm(forms.ModelForm):

    # Modelo de registro del formulario
    class Meta:
        model = ProductoModel.Solicitud
        fields = ['descripcion']
    
    # Definicion + validacion + style + label de campos
    descripcion = forms.CharField(validators=[
        validators.MinLengthValidator(0),
        validators.MaxLengthValidator(300)],
        widget=forms.Textarea(attrs={'class':'form-control','rows':'3'}),
        label='Descripcion',
        )
   
    



# # ~============= REGISTRO DE COMPRA =============~

# #ACA NO EH TOCADO ABSOLUTAMENTE NADA AUN

# # |===> CLASS RegistroCompra EDITAR [PK id_registro_compra | FK cliente_id, producto_id]
# class RegistroCompra(forms.Form):

#     # FK cliente
#     # producto_id = forms.ForeignKey(validators=[
#     #     validators.MinLengthValidator(3),
#     #     validators.MaxLengthValidator(25)
#     # ])
#     precio_total = forms.FloatField()
#     garantia = forms.BooleanField()
#     delivery = forms.BooleanField()
#     # fecha_compra = forms.DateTimeField(validators=[
#     #     validators.MinLengthValidator(3),
#     #     validators.MaxLengthValidator(25)
#     # ])

# # |===> style formulario de BS5 RegistroCompra

#     precio_total.widget.attrs['class'] = 'form-control'
#     garantia.widget.attrs['class'] = 'form-control'
#     delivery.widget.attrs['class'] = 'form-control'
#     # fecha_compra.widget.attrs['class'] = 'form-control'
    
#     # Tag para RegistroCompra personalizado
#     precio_total.label = 'Precio total'
#     garantia.label = 'Garantia'
#     delivery.label = 'Delivery'

#     class RegistroCompra(forms.ModelForm):
#         class Meta:
#             model = ProductoModel.Producto
#             fields = '__all__'
        
#         precio_total = forms.FloatField()
#         garantia = forms.BooleanField()
#         delivery = forms.BooleanField()
