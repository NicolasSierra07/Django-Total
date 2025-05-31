from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Modelo de usuario personalizado con campos organizados por categorías
class Usuario(AbstractUser):
    # Campos básicos de autenticación
    email = models.EmailField(_('email address'), unique=True)
    telefono = models.CharField(_('teléfono'), max_length=20, blank=True, null=True)
    direccion = models.CharField(_('dirección'), max_length=255, blank=True, null=True)
    fecha_registro = models.DateTimeField(_('fecha de registro'), auto_now_add=True)
    
    # Campos para ahorros y préstamos
    class Financiero(models.TextChoices):
        AHORROS = 'AH', _('Ahorros')
        PRESTAMOS = 'PR', _('Préstamos')
    
    tipo_financiero = models.CharField(
        max_length=2,
        choices=Financiero.choices,
        blank=True,
        null=True
    )
    saldo_ahorros = models.DecimalField(
        _('saldo de ahorros'),
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    
    # Campos para productos y vendedores
    class TipoVendedor(models.TextChoices):
        REGULAR = 'RV', _('Vendedor Regular')
        PREMIUM = 'PV', _('Vendedor Premium')
    
    tipo_vendedor = models.CharField(
        max_length=2,
        choices=TipoVendedor.choices,
        blank=True,
        null=True
    )
    calificacion = models.DecimalField(
        _('calificación'),
        max_digits=3,
        decimal_places=2,
        default=0.00
    )
    
    # Campos para productos_extra, reservas y restaurantes
    class TipoUsuarioRestaurante(models.TextChoices):
        CLIENTE = 'CL', _('Cliente')
        RESTAURANTE = 'RS', _('Restaurante')
    
    tipo_usuario_restaurante = models.CharField(
        max_length=2,
        choices=TipoUsuarioRestaurante.choices,
        blank=True,
        null=True
    )
    reservas_activas = models.IntegerField(
        _('reservas activas'),
        default=0
    )
    puntos_recompensa = models.IntegerField(
        _('puntos de recompensa'),
        default=0
    )
    
    def __str__(self):
        # Muestra el nombre de usuario
        return self.username

    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')
