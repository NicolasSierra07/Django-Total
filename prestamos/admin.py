from django.contrib import admin
from .models import Prestamo, Cuota

# Permite ver las cuotas como inlines en el préstamo
class CuotaInline(admin.TabularInline):
    model = Cuota
    extra = 0

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'monto', 'meses', 'tasa_interes_mensual', 'saldo_pendiente', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['usuario__username']
    inlines = [CuotaInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)

@admin.register(Cuota)
class CuotaAdmin(admin.ModelAdmin):
    list_display = ['numero_cuota', 'monto', 'capital', 'interes', 'fecha_vencimiento', 'estado', 'prestamo']
    list_filter = ['estado', 'fecha_vencimiento']
    search_fields = ['prestamo__usuario__username']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(prestamo__usuario=request.user)
    
    def capital(self, obj):
        return f"${obj.capital:.2f}"
    capital.short_description = 'Capital'
    
    def interes(self, obj):
        return f"${obj.interes:.2f}"
    interes.short_description = 'Interés'
