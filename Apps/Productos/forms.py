
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
        fields = ['comentario']

    # Definicion + validacion + style + label de campos
    comentario = forms.CharField(validators=[
        validators.MinLengthValidator(3),
        validators.MaxLengthValidator(300)],
        widget=forms.Textarea(attrs={'class':'form-control', 'rows': 3, 'placeholder': 'Escribe tu comentario aquí...'}),
        label='Comentario del producto'
    )
    
# |<><><><><><><><><><><><><><><><><><><><><><><><>|

# |===> Formulario de CREACION y EDICION <Calificacion>
class RegisterCalificacionForm(forms.ModelForm):

    # Modelo de registro del formulario
    class Meta:
        model = ProductoModel.Calificacion
        fields = {'cant_estrella'}

    # Definicion + validacion + style + label de campos
    cant_estrella = forms.IntegerField(validators=[
        validators.MinValueValidator(0),
        validators.MaxValueValidator(5)],
        widget=forms.NumberInput(attrs={'class':'form-control'}),
        label='Cantidad de estrellas'
    )

# ~============= SOLICITUDES =============~

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
   
    
