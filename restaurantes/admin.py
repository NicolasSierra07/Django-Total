from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import Restaurante
from usuarios.models import Usuario

@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'categoria', 'usuario')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'ubicacion')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Filtrar usuarios disponibles
        form.base_fields['usuario'].queryset = Usuario.objects.filter(
            tipo_usuario_restaurante='RS'
        )
        
        # Hacer el campo usuario requerido
        form.base_fields['usuario'].required = True
        
        return form

    def save_model(self, request, obj, form, change):
        usuario = form.cleaned_data.get('usuario')
        if usuario:
            obj.usuario = usuario
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "usuario":
            kwargs["queryset"] = Usuario.objects.filter(tipo_usuario_restaurante='RS')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
