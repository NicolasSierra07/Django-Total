from django.contrib import admin
from .models import Reserva

# Registra el modelo Reserva en el panel de administración
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'producto', 'estado')
    list_filter = ('estado',)
    search_fields = ('usuario__nombre', 'producto__nombre')
