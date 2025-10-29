from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.shipping.serializers.shipping_serializer import ShippingAddressSerializer
from apps.shipping.services.shipping_service import ShippingAddressService
from apps.shipping.models import ShippingAddress

class ShippingAddressViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    service_class = ShippingAddressService

    def list(self, request):
        svc = self.service_class()

        qs = svc.get_shipping_addresses(request.user)
        return Response(ShippingAddressSerializer(qs, many=True).data)
    
    def create(self, request):
        svc = self.service_class()
        user = request.user
        data = request.data

        if not user:
            return Response({'error', 'User does not exists.'}, status=404)
        if not data:
            return Response({'error', 'There is no data.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ShippingAddressSerializer(data=data)
        serializer.is_valid(raise_exception=True)


        new_address = svc.create_shipping_address(user, serializer.validated_data)

        return Response({
            'address': ShippingAddressSerializer(new_address).data,
            'message': 'Address created successfully.'
        },
        status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='update')
    def update_address(self, request, pk=None):
        svc = self.service_class()
        user = request.user
        data = request.data
        
        if not user:
            return Response({'error', 'User does not exists.'}, status=404)
        if not data:
            return Response({'error', 'There is no data.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ShippingAddressSerializer(data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_address = svc.update_shipping_address(user, serializer.validated_data, pk)

        return Response({
            'address': ShippingAddressSerializer(updated_address).data,
            'message': 'Address updated successfully.'
            })
    
    @action(detail=True, methods=['patch'], url_path='is-default')
    def update_address_is_default(self, request, pk=None):
        svc = self.service_class()
        user = request.user

        updated_user = svc.set_default_shipping_address(user, pk)

        serializer = ShippingAddressSerializer(updated_user)
        
        return Response({
            'address': serializer.data,
            'message': 'New default address set successfully.'
        })

    def destroy(self, request, pk=None):
        svc = self.service_class()
        user = request.user

        if not user:
            return Response({'error', 'User does not exists.'})
        
        try:
            svc.delete_shipping_address(user, pk)
            return Response({'message': 'Address deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    