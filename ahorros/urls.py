from django.urls import path
from .views import (
    CuentaAhorroListCreateView,           # Vista para listar y crear cuentas de ahorro
    CuentaAhorroRetrieveUpdateDestroyView, # Vista para obtener, actualizar o eliminar una cuenta de ahorro
    DepositarAhorroView,                  # Vista para depositar en una cuenta de ahorro
    RetirarAhorroView,                    # Vista para retirar de una cuenta de ahorro
)

# Definición de las rutas de la app ahorros
urlpatterns = [
    # Listar todas las cuentas o crear una nueva
    path('cuentas/', CuentaAhorroListCreateView.as_view(), name='cuentaahorro-list-create'),
    # Obtener, actualizar o eliminar una cuenta específica por su ID
    path('cuentas/<int:pk>/', CuentaAhorroRetrieveUpdateDestroyView.as_view(), name='cuentaahorro-detail'),
    # Realizar un depósito en una cuenta (requiere ID por body o query param)
    path('depositar/', DepositarAhorroView.as_view(), name='depositar-ahorro'),
    # Realizar un retiro de una cuenta (requiere ID por body o query param)
    path('retirar/', RetirarAhorroView.as_view(), name='retirar-ahorro'),
]