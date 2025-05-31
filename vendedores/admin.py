from django.contrib import admin
from .models import Vendedor

@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('nombre_tienda', 'usuario')
    list_filter = ('nombre_tienda',)
    search_fields = ('nombre_tienda', 'usuario__username')
    fieldsets = (
        (None, {
            'fields': ('usuario', 'nombre_tienda', 'direccion')
        }),
    )
    
    def get_fieldsets(self, request, obj=None):
        return self.fieldsets

    def get_form(self, request, obj=None, **kwargs):
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)