from django.db import models
from django.conf import settings

# Usamos settings.AUTH_USER_MODEL para evitar importaciones circulares
Usuario = settings.AUTH_USER_MODEL
from productos.models import Producto

class Reserva(models.Model):
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    )

    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, limit_choices_to={'tipo_usuario_restaurante': 'CL'})
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, limit_choices_to={'tipo': 'RESTAURANTE'})
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    
    def clean(self):
        from django.core.exceptions import ValidationError
        # Validar que el producto sea de tipo RESTAURANTE
        if self.producto and self.producto.tipo != 'RESTAURANTE':
            raise ValidationError({'producto': 'Solo se pueden reservar productos de restaurante.'})
        
        # Validar que el producto tenga un restaurante asignado
        if self.producto and not self.producto.restaurante:
            raise ValidationError({'producto': 'El producto debe tener un restaurante asignado.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario.username if hasattr(self.usuario, 'username') else self.usuario} - {self.producto.nombre}"
