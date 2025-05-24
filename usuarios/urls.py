from django.urls import path
from .views import (
    UsuarioListCreateView,           # Vista para listar y crear usuarios
    UsuarioRetrieveUpdateDestroyView # Vista para obtener, actualizar o eliminar un usuario
)

# Rutas de la app usuarios
urlpatterns = [
    # Listar todos los usuarios o crear uno nuevo
    path('usuarios/', UsuarioListCreateView.as_view(), name='usuario-list-create'),
    # Obtener, actualizar o eliminar un usuario específico
    path('usuarios/<int:pk>/', UsuarioRetrieveUpdateDestroyView.as_view(), name='usuario-detail'),
]