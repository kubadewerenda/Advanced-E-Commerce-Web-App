from rest_framework import status, viewsets, permissions
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.orders.models import PaymentMethod, PaymentProvider
from apps.payments.services.payment_service import PaymentService
from apps.payments.serializers.payment_serializer import PaymentItemSerializer

class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    service_class = PaymentService

    @action(detail=False, methods=['get'], url_path='payment_methods')
    def get_payment_methods(self, request):
        resp = self.service_class().get_list_of_payment_methods()

        return Response(PaymentItemSerializer(resp, many=True).data)

    # --- TODO: ---
    # 1. Do rest of payment views