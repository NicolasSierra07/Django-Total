from django.db import models
from usuarios.models import Usuario
from django.core.exceptions import ValidationError

class Restaurante(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        related_name='restaurantes',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Restaurante'
        verbose_name_plural = 'Restaurantes'
        ordering = ['nombre']
