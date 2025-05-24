from django.contrib import admin
from .models import Usuario

# Admin para el modelo Usuario
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_active']
    search_fields = ['username', 'email']
