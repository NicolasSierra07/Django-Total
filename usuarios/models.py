from django.db import models
from django.contrib.auth.models import AbstractUser

# Modelo de usuario personalizado (puedes agregar más campos si lo necesitas)
class Usuario(AbstractUser):
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Muestra el nombre de usuario
        return self.username
