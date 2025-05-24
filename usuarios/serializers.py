from rest_framework import serializers
from .models import Usuario

# Serializador para el modelo Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'