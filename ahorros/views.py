from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CuentaAhorro, MovimientoAhorro
from .serializers import CuentaAhorroSerializer, MovimientoAhorroSerializer
from django.utils import timezone

# Listar y crear cuentas de ahorro
class CuentaAhorroListCreateView(generics.ListCreateAPIView):
    queryset = CuentaAhorro.objects.all()
    serializer_class = CuentaAhorroSerializer

# Obtener, actualizar o eliminar una cuenta de ahorro específica
class CuentaAhorroRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CuentaAhorro.objects.all()
    serializer_class = CuentaAhorroSerializer

# Realizar un depósito en una cuenta de ahorro
class DepositarAhorroView(APIView):
    def post(self, request, pk):
        try:
            cuenta = CuentaAhorro.objects.get(pk=pk)
            monto = request.data.get('monto')

            # Validar que se envíe un monto
            if not monto:
                return Response({'error': 'Monto requerido'}, status=status.HTTP_400_BAD_REQUEST)
            # Validar que el monto no sea negativo
            if float(monto) < 0:
                return Response({'error': 'El monto no puede ser negativo'}, status=status.HTTP_400_BAD_REQUEST)

            hoy = timezone.now()
            # Calcular meses consecutivos de ahorro
            if cuenta.ultimo_deposito:
                dias_transcurridos = (hoy - cuenta.ultimo_deposito).days
                if dias_transcurridos > 31:
                    cuenta.meses_ahorro_consecutivo = 1
                else:
                    cuenta.meses_ahorro_consecutivo += 1
            else:
                cuenta.meses_ahorro_consecutivo = 1

            # Registrar el movimiento de depósito
            MovimientoAhorro.objects.create(
                cuenta=cuenta,
                monto=monto,
                tipo='DEPOSITO'
            )

            # Actualizar saldo y fecha del último depósito
            cuenta.saldo += float(monto)
            cuenta.ultimo_deposito = hoy

            # Si cumple 12 meses consecutivos, aumentar tasa de interés y registrar bonificación
            if cuenta.meses_ahorro_consecutivo >= 12 and cuenta.tasa_interes < 7:
                cuenta.tasa_interes = 7.00
                MovimientoAhorro.objects.create(
                    cuenta=cuenta,
                    monto=0,
                    tipo='INTERES',
                    descripcion='Aumento de tasa por ahorro consecutivo'
                )

            cuenta.save()
            return Response({'message': 'Depósito realizado exitosamente'})
        except CuentaAhorro.DoesNotExist:
            return Response({'error': 'Cuenta no encontrada'}, status=status.HTTP_404_NOT_FOUND)

# Realizar un retiro de una cuenta de ahorro
class RetirarAhorroView(APIView):
    def post(self, request, pk):
        try:
            cuenta = CuentaAhorro.objects.get(pk=pk)
        except CuentaAhorro.DoesNotExist:
            return Response({'error': 'Cuenta no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        monto = request.data.get('monto')
        # Validar que se envíe un monto
        if not monto:
            return Response({'error': 'Monto requerido'}, status=status.HTTP_400_BAD_REQUEST)
        # Validar que el saldo sea suficiente
        if float(monto) > cuenta.saldo:
            return Response({'error': 'Saldo insuficiente'}, status=status.HTTP_400_BAD_REQUEST)

        # Registrar el movimiento de retiro
        MovimientoAhorro.objects.create(
            cuenta=cuenta,
            monto=monto,
            tipo='RETIRO'
        )

        # Actualizar saldo
        cuenta.saldo -= float(monto)
        cuenta.save()
        return Response({'message': 'Retiro realizado exitosamente'})
