from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('usuarios.urls')),
    path('api/prestamos/', include('prestamos.urls')),
    path('api/ahorros/', include('ahorros.urls')),
    path('api/productos/', include('productos.urls')),
    path('api/vendedores/', include('vendedores.urls')),
    path('api/restaurantes/', include('restaurantes.urls')),
    path('api/reservas/', include('reservas.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
