from django.db import models
from django.core.exceptions import ValidationError
from usuarios.models import Usuario

# Modelo de cuenta de ahorro
class CuentaAhorro(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='cuenta_ahorro')
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tasa_interes = models.DecimalField(max_digits=4, decimal_places=2, default=6.00)
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    meses_ahorro_consecutivo = models.IntegerField(default=0)
    ultimo_deposito = models.DateTimeField(null=True, blank=True)
    interes_acumulado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        # Mostrar el nombre del usuario en vez de CuentaAhorro object (x)
        return str(self.usuario)

    def clean(self):
        # Validar que el saldo no sea menor al mínimo
        if self.saldo < self.saldo_minimo:
            raise ValidationError(f'El saldo no puede ser menor a {self.saldo_minimo}')

# Modelo de movimientos de ahorro (depósitos, retiros, intereses)
class MovimientoAhorro(models.Model):
    cuenta = models.ForeignKey(CuentaAhorro, on_delete=models.CASCADE, related_name='movimientos')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=[
        ('DEPOSITO', 'Depósito'),
        ('RETIRO', 'Retiro'),
        ('INTERES', 'Interés')
    ])
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Al crear un movimiento, actualizar el saldo de la cuenta
        if self.pk is None:
            if self.tipo == 'DEPOSITO':
                self.cuenta.saldo += self.monto
            elif self.tipo == 'RETIRO':
                self.cuenta.saldo -= self.monto
            self.cuenta.save()
        super().save(*args, **kwargs)

    def __str__(self):
        # Mostrar el usuario y el tipo de movimiento
        return f"{self.cuenta.usuario} - {self.get_tipo_display()} - {self.monto}"
