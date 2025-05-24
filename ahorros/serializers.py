from rest_framework import serializers
from .models import CuentaAhorro, MovimientoAhorro

# Serializador para movimientos de ahorro
class MovimientoAhorroSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoAhorro
        fields = '__all__'

# Serializador para cuentas de ahorro, incluye los movimientos
class CuentaAhorroSerializer(serializers.ModelSerializer):
    movimientos = MovimientoAhorroSerializer(many=True, read_only=True)

    class Meta:
        model = CuentaAhorro
        fields = '__all__'