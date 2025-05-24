from django.contrib import admin
from .models import Prestamo, Cuota, Mora

# Permite ver las cuotas como inlines en el préstamo
class CuotaInline(admin.TabularInline):
    model = Cuota
    extra = 0

# Permite ver la mora como inline en la cuota
class MoraInline(admin.TabularInline):
    model = Mora
    extra = 0

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'monto', 'meses', 'saldo_pendiente', 'cuota_mensual', 'fecha_creacion']
    list_filter = ['fecha_creacion']  # Solo deja campos que existan en Prestamo
    search_fields = ['usuario__username']
    inlines = [CuotaInline]

@admin.register(Cuota)
class CuotaAdmin(admin.ModelAdmin):
    list_display = ['prestamo', 'numero_cuota', 'monto', 'fecha_vencimiento', 'estado']
    list_filter = ['estado', 'fecha_vencimiento']
    search_fields = ['prestamo__usuario__username']
    inlines = [MoraInline]

@admin.register(Mora)
class MoraAdmin(admin.ModelAdmin):
    list_display = ['cuota', 'monto', 'fecha_generacion']
