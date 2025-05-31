from django.contrib import admin
from django.utils.html import format_html
from .models import Producto

class StockFilter(admin.SimpleListFilter):
    title = 'Estado de Stock'
    parameter_name = 'estado_stock'

    def lookups(self, request, model_admin):
        return (
            ('bajo', 'Stock Bajo (<5)'),
            ('medio', 'Stock Medio (5-20)'),
            ('alto', 'Stock Alto (>20)'),
        )

    def queryset(self, request, queryset):
        # No aplicar ningún filtro si no se seleccionó un valor
        if self.value() is None:
            return queryset
        
        # Solo aplicar a productos que tengan stock
        if self.value() == 'bajo':
            return queryset.filter(stock__lt=5, stock__isnull=False)
        if self.value() == 'medio':
            return queryset.filter(stock__gte=5, stock__lte=20, stock__isnull=False)
        if self.value() == 'alto':
            return queryset.filter(stock__gt=20, stock__isnull=False)
        return queryset

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'get_tipo_display', 'get_relacion', 'precio', 'get_stock_colored')
    list_filter = ('tipo', StockFilter)
    search_fields = ('nombre', 'descripcion')
    
    # Aseguramos que el admin muestre todos los tipos de productos
    def changelist_view(self, request, extra_context=None):
        # Eliminamos cualquier filtro que pueda estar limitando los resultados
        q = request.GET.copy()
        # Aseguramos que no haya filtros ocultos
        if 'tipo__exact' in q:
            del q['tipo__exact']
        request.GET = q
        return super().changelist_view(request, extra_context=extra_context)
    
    def get_fieldsets(self, request, obj=None):
        # Campos base que siempre se muestran
        fieldsets = [
            ('Información Básica', {
                'fields': ('nombre', 'descripcion', 'precio', 'tipo')
            }),
        ]
        
        # Campos específicos según el tipo
        if obj is None or obj.tipo == 'VENDEDOR':
            fieldsets.append(('Información de Vendedor', {
                'fields': ('vendedor', 'stock'),
                'classes': ('collapse',) if obj and obj.tipo != 'VENDEDOR' else tuple()
            }))
            
        if obj is None or obj.tipo == 'RESTAURANTE':
            fieldsets.append(('Información de Restaurante', {
                'fields': ('restaurante',),
                'classes': ('collapse',) if obj and obj.tipo != 'RESTAURANTE' else tuple()
            }))
            
        return fieldsets
    
    def get_tipo_display(self, obj):
        return obj.get_tipo_display()
    get_tipo_display.short_description = 'Tipo'
    
    def get_relacion(self, obj):
        if obj.tipo == 'VENDEDOR' and obj.vendedor:
            return obj.vendedor.nombre_tienda
        elif obj.tipo == 'RESTAURANTE' and obj.restaurante:
            return obj.restaurante.nombre
        return '-'
    get_relacion.short_description = 'Relacionado con'
    
    def get_stock_colored(self, obj):
        if obj.tipo != 'VENDEDOR' or obj.stock is None:
            return '-'
        
        if obj.stock < 5:
            color = 'red'
        elif obj.stock < 20:
            color = 'orange'
        else:
            color = 'green'
        
        return format_html('<span style="color: {};"><b>{}</b></span>', color, obj.stock)
    get_stock_colored.short_description = 'Stock'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Imprimir para depuración
        print(f"Total de productos: {qs.count()}")
        print(f"Productos de vendedor: {qs.filter(tipo='VENDEDOR').count()}")
        print(f"Productos de restaurante: {qs.filter(tipo='RESTAURANTE').count()}")
        
        # Si no es superusuario, filtrar por tipo según permisos
        if not request.user.is_superuser:
            if hasattr(request.user, 'vendedor') and request.user.vendedor:
                return qs.filter(vendedor=request.user.vendedor)
            elif hasattr(request.user, 'restaurante') and request.user.restaurante:
                return qs.filter(restaurante=request.user.restaurante)
            return qs.none()
        return qs
