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

    @property
    def total_con_rentabilidad(self):
        """Calcula el total con la rentabilidad anual aplicada"""
        return self.saldo + (self.saldo * self.tasa_interes / 100)

    @property
    def rentabilidad_anual(self):
        """Devuelve la tasa de interés anual como porcentaje"""
        return f"{self.tasa_interes}"

    @property
    def bonificacion_activa(self):
        """Indica si tiene bonificación por ahorro consecutivo"""
        return self.tasa_interes == 7.00

    @property
    def meses_para_bonificacion(self):
        """Calcula cuántos meses faltan para la bonificación"""
        if self.tasa_interes == 6.00:
            return 12 - self.meses_ahorro_consecutivo
        return 0

    def __str__(self):
        # Mostrar el nombre del usuario en vez de CuentaAhorro object (x)
        return str(self.usuario)

    def clean(self):
        # Validar que el saldo no sea menor al mínimo
        if self.saldo < self.saldo_minimo:
            raise ValidationError(f'El saldo no puede ser menor a {self.saldo_minimo}')

    def actualizar_meses_consecutivos(self):
        """Actualiza los meses consecutivos basado en el último movimiento"""
        from django.utils import timezone
        ultimo_movimiento = self.movimientos.order_by('-fecha').first()
        if ultimo_movimiento:
            dias_transcurridos = (timezone.now() - ultimo_movimiento.fecha).days
            if dias_transcurridos <= 31:
                self.meses_ahorro_consecutivo += 1
            else:
                self.meses_ahorro_consecutivo = 1
        else:
            self.meses_ahorro_consecutivo = 1

        # Si cumple 12 meses consecutivos y no tiene bonificación, aplicarla
        if self.meses_ahorro_consecutivo >= 12 and self.tasa_interes == 6.00:
            self.tasa_interes = 7.00
            self.save(update_fields=['tasa_interes'])
            MovimientoAhorro.objects.create(
                cuenta=self,
                monto=0,
                tipo='INTERES',
                descripcion='Aumento de tasa por ahorro consecutivo'
            )

    def save(self, *args, **kwargs):
        """Sobrescribir el método save para actualizar los meses consecutivos"""
        super().save(*args, **kwargs)
        self.actualizar_meses_consecutivos()

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
        
        # Actualizar los meses consecutivos después de cada movimiento
        self.cuenta.save()

    def __str__(self):
        # Mostrar el usuario y el tipo de movimiento
        return f"{self.cuenta.usuario} - {self.get_tipo_display()} - {self.monto}"
