from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from apps.orders.serializers.order_serializer import OrderSerializer, OrderCheckoutSerializer
from apps.orders.services.order_service import OrderService
from apps.orders.models import Order

class OrderViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    service_class = OrderService

    def list(self, request):
        qs = self.service_class().get_orders_for_user(request.user)
        return Response(OrderSerializer(qs, many=True).data)
    
    def retrieve(self, request, pk=None):
        qs = self.service_class().get_order_for_user(request.user, pk)
        return Response(OrderSerializer(qs).data)
    
    @action(detail=False, methods=['post'], url_path='create-from-cart', permission_classes=[permissions.AllowAny])
    def create_from_cart(self, request):
        serializer = OrderCheckoutSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = self.service_class().create_from_cart(request.user, serializer.validated_data)
        return Response({'order': OrderSerializer(order).data}, status=status.HTTP_201_CREATED)
    