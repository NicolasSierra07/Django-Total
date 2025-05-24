from django.db import models
from usuarios.models import Usuario

# Modelo de préstamo
class Prestamo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='prestamos')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    meses = models.IntegerField()
    saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cuota_mensual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Muestra el usuario y el monto del préstamo
        return f"{self.usuario} - ${self.monto} - {self.meses} meses"

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

    def __str__(self):
        # Muestra el número de cuota y el préstamo asociado
        return f"Cuota {self.numero_cuota} de {self.prestamo}"

# Modelo de mora asociada a una cuota
class Mora(models.Model):
    cuota = models.OneToOneField('Cuota', on_delete=models.CASCADE, related_name='mora')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_generacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Muestra la cuota y el monto de la mora
        return f"Mora de {self.cuota} - ${self.monto}"
