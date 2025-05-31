from django.urls import path
from .views import ReservaListCreate, ReservaDetail, ReservaDetalle

urlpatterns = [
    path('reservas/', ReservaListCreate.as_view(), name="reserva-list-create"),
    path('reservas/<int:pk>/', ReservaDetail.as_view(), name="reserva-detail"),
    path('reservas/crear/', ReservaDetalle.as_view(), name="reserva-create"),
]
