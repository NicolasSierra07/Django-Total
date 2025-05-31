from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = [
        'username', 'email', 'telefono', 'is_staff', 'is_active',
        'tipo_financiero', 'saldo_ahorros',
        'tipo_vendedor', 'calificacion',
        'tipo_usuario_restaurante', 'reservas_activas', 'puntos_recompensa'
    ]
    search_fields = ['username', 'email', 'telefono']
    list_filter = [
        'is_staff', 'is_active',
        'tipo_financiero', 'tipo_vendedor', 'tipo_usuario_restaurante'
    ]
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'email', 'telefono', 'direccion')
        }),
        ('Permisos', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Financiero', {
            'fields': ('tipo_financiero', 'saldo_ahorros')
        }),
        ('Vendedor', {
            'fields': ('tipo_vendedor', 'calificacion')
        }),
        ('Restaurante', {
            'fields': ('tipo_usuario_restaurante', 'reservas_activas', 'puntos_recompensa')
        }),
        ('Fechas importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'telefono', 'direccion',
                'tipo_financiero', 'tipo_vendedor', 'tipo_usuario_restaurante'
            ),
        }),
    )
