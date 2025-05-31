from django.db import models
from django.utils import timezone
from django.conf import settings

# Evitamos importaciones circulares
Usuario = settings.AUTH_USER_MODEL

class Producto(models.Model):
    # Campos comunes
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    
    # Tipo de producto
    TIPO_CHOICES = [
        ('VENDEDOR', 'Producto de Vendedor'),
        ('RESTAURANTE', 'Producto de Restaurante'),
    ]
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='VENDEDOR')
    
    # Relaciones opcionales (pueden ser nulas según el tipo)
    vendedor = models.ForeignKey('vendedores.Vendedor', on_delete=models.CASCADE, 
                              related_name='productos', null=True, blank=True)
    restaurante = models.ForeignKey('restaurantes.Restaurante', on_delete=models.CASCADE, 
                                 related_name='productos', null=True, blank=True)
    
    # Campos específicos para productos de vendedor
    stock = models.IntegerField(default=0, null=True, blank=True)
    
    def __str__(self):
        if self.tipo == 'VENDEDOR' and self.vendedor:
            return f'{self.nombre} - {self.vendedor.nombre_tienda}'
        elif self.tipo == 'RESTAURANTE' and self.restaurante:
            return f'{self.nombre} - {self.restaurante.nombre}'
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Asegurar consistencia en los campos según el tipo de producto
        if self.tipo == 'VENDEDOR':
            # Para productos de vendedor, aseguramos que restaurante sea None
            self.restaurante = None
            # Aseguramos que el stock tenga un valor por defecto si es None
            if self.stock is None:
                self.stock = 0
        elif self.tipo == 'RESTAURANTE':
            # Para productos de restaurante, aseguramos que vendedor sea None
            self.vendedor = None
            # Y que stock sea None ya que no aplica
            self.stock = None
            
        # Validación adicional para asegurar que las relaciones existan
        if self.tipo == 'VENDEDOR' and not self.vendedor:
            raise ValueError("Los productos de vendedor deben tener un vendedor asignado")
        if self.tipo == 'RESTAURANTE' and not self.restaurante:
            raise ValueError("Los productos de restaurante deben tener un restaurante asignado")
            
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
