from django.db import models
from django.contrib.auth.models import AbstractUser

# -MODELS -> USUARIOS

from django.contrib.auth.models import UserManager

class UsuarioManager(UserManager):
    """Sobrescribe el Manager para asegurar que el rol se asigne
       correctamente al crear superusuarios."""
    
    def create_superuser(self, username, email, password, **extra_fields):
        # Llama a la implementación base y luego asegura el rol
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', Usuario.ROL_ADMIN) # ¡Aquí está la magia!

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

    def is_client(self):
        return self.rol == self.ROL_CLIENTE

    def is_custom_admin(self):
        return self.rol == self.ROL_ADMIN
    
    # ~contructor
    def __str__(self):
        return self.username or self.email or f"Usuario {self.id}"
