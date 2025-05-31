from django.db import models
from usuarios.models import Usuario
from django.utils import timezone

class Vendedor(models.Model):
    # Relación 1 a 1 con Usuario
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE,
        related_name='vendedor'
    )
    nombre_tienda = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)
    calificacion_promedio = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        # Mostrar nombre de tienda y username del usuario relacionado
        return f'{self.nombre_tienda} ({self.usuario.username})'

    def save(self, *args, **kwargs):
        # Aseguramos que el usuario esté guardado antes de crear el vendedor
        if not self.usuario.pk:
            self.usuario.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'
        ordering = ['-fecha_registro']
