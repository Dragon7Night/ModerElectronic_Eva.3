from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password

# -MODELS -> USUARIOS

class Usuario(AbstractUser):

    # DEFINICION DE CONSTANTES (roles en la DB)
    ROL_CLIENTE = "client"
    ROL_ADMIN = "admin"

    # opciones que se pueden seleccionar en los roles
    OPCIONES_ROL = [
        (ROL_CLIENTE, "Cliente"),
        (ROL_ADMIN, "Administrador"),
    ]

    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=90)
    rol = models.CharField(max_length=15, choices=OPCIONES_ROL, default=ROL_CLIENTE)
    billetera = models.FloatField(default=0.0, blank=True)

    def is_client(self):
        return self.rol == self.ROL_CLIENTE

    def is_custom_admin(self):
        return self.rol == self.ROL_ADMIN
    
    # ~contructor
    def __str__(self):
        return self.username or self.email or f"Usuario {self.id}"


class ClaveAcceso(models.Model):
    clave_acceso = models.CharField(max_length=128)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def establecerClave(self, clave_pura):
        self.clave_acceso = make_password(clave_pura)
        self.save(update_fields=["clave_acceso"])

    def verificarClave(self, clave_pura):
        return check_password(clave_pura, self.clave_acceso)

    def __str__(self):
        return f"ClaveAcceso {self.id}"






