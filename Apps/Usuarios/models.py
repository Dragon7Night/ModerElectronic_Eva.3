
# '======[Importaciones]============================'
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import UserManager
# '================================================='

# °===========================°
#    °Modelo -> Usuarios
# °===========================°

class UsuarioManager(UserManager):
    # Astraccion de class ↑↑ linea 163
    """Sobrescribe el Manager para asegurar que el rol se asigne
       correctamente al crear superusuarios. De caso contrario se registran
       todo los users con el rol cliente, por defecto"""
    
    def create_superuser(self, username, email, password, **extra_fields):
        # Si el user tiene staff y superuser en True se le asigna por defecto el rol Admin
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', Usuario.ROL_ADMIN)

        # Mensajes de error
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')
        
        return self._create_user(username, email, password, **extra_fields)


class Usuario(AbstractUser):

    # DEFINICION DE CONSTANTES (roles en la DB)
    ROL_CLIENTE = "client"
    ROL_ADMIN = "admin"

    # opciones que se pueden seleccionar en los roles
    OPCIONES_ROL = [
        (ROL_CLIENTE, "Cliente"),
        (ROL_ADMIN, "Administrador"),
    ]

    direccion = models.CharField(max_length=90)
    rol = models.CharField(max_length=15, choices=OPCIONES_ROL, default=ROL_CLIENTE)
    billetera = models.FloatField(default=0.0, blank=True)

    objects = UsuarioManager() 

    @property
    def is_client(self):
        return self.rol == self.ROL_CLIENTE

    @property
    def is_custom_admin(self):
        return self.rol == self.ROL_ADMIN
    
    # ~contructor
    def __str__(self):
        return self.username or self.email or f"Usuario {self.id}"


