from rest_framework import generics
from .models import Usuario
from .serializers import UsuarioSerializer

# Listar y crear usuarios
class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# Obtener, actualizar o eliminar un usuario específico
class UsuarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
