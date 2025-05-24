from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Prestamo, Cuota, Mora
from .serializers import PrestamoSerializer
from datetime import date
from dateutil.relativedelta import relativedelta

# Listar y crear préstamos
class PrestamoListCreateView(generics.ListCreateAPIView):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer

    # Al crear un préstamo, genera las cuotas automáticamente
    def perform_create(self, serializer):
        prestamo = serializer.save()
        prestamo.saldo_pendiente = prestamo.monto
        prestamo.save()
        monto_cuota = prestamo.monto / prestamo.meses
        fecha_inicio = date.today()
        for i in range(prestamo.meses):
            fecha_vencimiento = fecha_inicio + relativedelta(months=i)
            Cuota.objects.create(
                prestamo=prestamo,
                numero_cuota=i + 1,
                monto=monto_cuota,
                fecha_vencimiento=fecha_vencimiento
            )

# Obtener, actualizar o eliminar un préstamo específico
class PrestamoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer

# Pagar una cuota de un préstamo
class PagarCuotaView(APIView):
    def post(self, request, pk):
        try:
            prestamo = Prestamo.objects.get(pk=pk)
            cuota_id = request.data.get('cuota_id')
            cuota = Cuota.objects.get(id=cuota_id, prestamo=prestamo)

            if cuota.estado == 'PAGADA':
                return Response({'error': 'La cuota ya está pagada'}, status=status.HTTP_400_BAD_REQUEST)

            cuota.fecha_pago = date.today()
            cuota.estado = 'PAGADA'
            cuota.save()

            # Disminuir saldo pendiente
            prestamo.saldo_pendiente = max(prestamo.saldo_pendiente - cuota.monto, 0)
            prestamo.save()

            return Response({'message': 'Cuota pagada y saldo actualizado'})
        except (Prestamo.DoesNotExist, Cuota.DoesNotExist):
            return Response({'error': 'Préstamo o cuota no encontrada'}, status=status.HTTP_404_NOT_FOUND)
