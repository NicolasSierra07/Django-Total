from django.urls import path
from .views import RestauranteListCreate, RestauranteDetail, RestauranteDetalle

urlpatterns = [
    path('restaurantes/', RestauranteListCreate.as_view(), name="restaurante-list-create"),
    path('restaurantes/<int:pk>/', RestauranteDetail.as_view(), name="restaurante-detail"),
    path('restaurantes/crear/', RestauranteDetalle.as_view(), name="restaurante-create"),
]
