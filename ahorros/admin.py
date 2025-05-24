from django.contrib import admin
from .models import CuentaAhorro, MovimientoAhorro

# Permite ver los movimientos como inlines en la cuenta de ahorro
class MovimientoAhorroInline(admin.TabularInline):
    model = MovimientoAhorro
    extra = 0

# Admin de cuenta de ahorro
@admin.register(CuentaAhorro)
class CuentaAhorroAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'saldo', 'tasa_interes', 'meses_ahorro_consecutivo']
    search_fields = ['usuario__username']
    inlines = [MovimientoAhorroInline]

# Admin de movimientos de ahorro
@admin.register(MovimientoAhorro)
class MovimientoAhorroAdmin(admin.ModelAdmin):
    list_display = ['cuenta', 'monto', 'tipo', 'fecha']
    list_filter = ['tipo', 'fecha']
    search_fields = ['cuenta__usuario__username']