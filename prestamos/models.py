from django.db import models
from usuarios.models import Usuario
from decimal import Decimal
from dateutil.relativedelta import relativedelta

# Modelo de préstamo con tabla de amortización francesa
class Prestamo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='prestamos')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    meses = models.IntegerField()
    tasa_interes_mensual = models.DecimalField(max_digits=5, decimal_places=2, default=2.50)
    saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def calcular_cuota_mensual(self):
        """Calcula la cuota mensual usando la fórmula de amortización francesa"""
        tasa = self.tasa_interes_mensual / Decimal('100.00')
        numerador = self.monto * tasa * (1 + tasa) ** self.meses
        denominador = (1 + tasa) ** self.meses - 1
        return round(numerador / denominador, 2)

    def generar_cuotas(self):
        """Genera todas las cuotas del préstamo"""
        cuota_mensual = self.calcular_cuota_mensual()
        saldo = self.monto
        fecha = self.fecha_creacion

        for mes in range(1, self.meses + 1):
            interes = saldo * (self.tasa_interes_mensual / Decimal('100.00'))
            capital = cuota_mensual - interes
            saldo -= capital

            Cuota.objects.create(
                prestamo=self,
                numero_cuota=mes,
                monto=cuota_mensual,
                fecha_vencimiento=fecha.date(),
                estado='PENDIENTE'
            )
            fecha = fecha.replace(day=1) + relativedelta(months=1)

    def __str__(self):
        return f"{self.usuario} - ${self.monto} - {self.meses} meses"

    def save(self, *args, **kwargs):
        """Sobrescribir save para generar cuotas automáticamente"""
        super().save(*args, **kwargs)
        if not self.cuotas.exists():  # Solo generar cuotas si es nuevo préstamo
            self.generar_cuotas()

# Modelo de cuota de préstamo
class Cuota(models.Model):
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE, related_name='cuotas')
    numero_cuota = models.IntegerField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    fecha_pago = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=[
        ('PENDIENTE', 'Pendiente'),
        ('PAGADA', 'Pagada'),
        ('VENCIDA', 'Vencida')
    ])

    @property
    def interes(self):
        """Calcula el interés de la cuota"""
        return self.monto * (self.prestamo.tasa_interes_mensual / 100)

    @property
    def capital(self):
        """Calcula el capital de la cuota"""
        return self.monto - self.interes

    def save(self, *args, **kwargs):
        """Sobrescribir save para actualizar el saldo del préstamo"""
        super().save(*args, **kwargs)
        if self.estado == 'PAGADA':
            self.prestamo.saldo_pendiente -= self.capital
            self.prestamo.save()

    def __str__(self):
        return f"Cuota {self.numero_cuota} de {self.prestamo}"
