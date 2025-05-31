from django.contrib import admin
from .models import CuentaAhorro, MovimientoAhorro

# Permite ver los movimientos como inlines en la cuenta de ahorro
class MovimientoAhorroInline(admin.TabularInline):
    model = MovimientoAhorro
    extra = 0

# Admin de cuenta de ahorro
@admin.register(CuentaAhorro)
class CuentaAhorroAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'saldo', 'total_con_rentabilidad', 'rentabilidad_anual', 'bonificacion_activa', 'meses_para_bonificacion', 'meses_ahorro_consecutivo']
    search_fields = ['usuario__username']
    inlines = [MovimientoAhorroInline]
    
    def total_con_rentabilidad(self, obj):
        return f"${obj.total_con_rentabilidad:.2f}"
    total_con_rentabilidad.short_description = 'Total con Rentabilidad'
    
    def rentabilidad_anual(self, obj):
        return f"{obj.rentabilidad_anual}"
    rentabilidad_anual.short_description = 'Rentabilidad Anual'
    
    def bonificacion_activa(self, obj):
        return 'Sí' if obj.bonificacion_activa else 'No'
    bonificacion_activa.short_description = 'Bonificación Activa'
    
    def meses_para_bonificacion(self, obj):
        if obj.meses_para_bonificacion > 0:
            return f"{obj.meses_para_bonificacion} meses"
        return 'Bonificación alcanzada'
    meses_para_bonificacion.short_description = 'Meses para Bonificación'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)

# Admin de movimientos de ahorro
@admin.register(MovimientoAhorro)
class MovimientoAhorroAdmin(admin.ModelAdmin):
    list_display = ['cuenta', 'monto', 'tipo', 'fecha']
    list_filter = ['tipo', 'fecha']
    search_fields = ['cuenta__usuario__username']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(cuenta__usuario=request.user)