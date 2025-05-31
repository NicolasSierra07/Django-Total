from django.urls import path
from .views import (
    UsuarioListCreateView,
    UsuarioRetrieveUpdateDestroyView
)

# Rutas de la app usuarios
urlpatterns = [
    # Rutas de API
    path('usuarios/', UsuarioListCreateView.as_view(), name='usuario-list-create'),
    path('usuarios/<int:pk>/', UsuarioRetrieveUpdateDestroyView.as_view(), name='usuario-detail'),
]
