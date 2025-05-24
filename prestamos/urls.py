from django.urls import path
from .views import (
    PrestamoListCreateView,
    PrestamoRetrieveUpdateDestroyView,
    PagarCuotaView,
)

# Rutas de la app prestamos
urlpatterns = [
    # Listar todos los préstamos o crear uno nuevo
    path('prestamos/', PrestamoListCreateView.as_view(), name='prestamo-list-create'),
    # Obtener, actualizar o eliminar un préstamo específico
    path('prestamos/<int:pk>/', PrestamoRetrieveUpdateDestroyView.as_view(), name='prestamo-detail'),
    # Pagar una cuota de un préstamo
    path('prestamos/<int:pk>/pagar-cuota/', PagarCuotaView.as_view(), name='pagar-cuota'),
]