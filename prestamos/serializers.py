from rest_framework import serializers
from .models import Prestamo, Cuota, Mora

# Serializador para cuotas
class CuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuota
        fields = '__all__'

# Serializador para moras
class MoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mora
        fields = '__all__'

# Serializador para préstamos, incluye cuotas y moras
class PrestamoSerializer(serializers.ModelSerializer):
    cuotas = CuotaSerializer(many=True, read_only=True)

    class Meta:
        model = Prestamo
        fields = '__all__'