from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from apps.cart.serializers.cart_serializer import CartSerializer, CartItemSerializer, CartNumItemsSerializer
from apps.cart.services.cart_service import CartService
from apps.cart.models import Cart


class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    service_class = CartService  

    @action(detail=False, methods=['post'], url_path='add')
    def add_to_cart(self, request):
        svc = self.service_class()
        cart_code = request.data.get('cart_code')
        variant_sku = request.data.get('variant_sku')
        try:
            quantity = int(request.data.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 1

        if not variant_sku:
            return Response({'error': 'There is not variant sku in params.'}, status=400)

        try:
            result = svc.add_item(request.user, cart_code, variant_sku, quantity)
        except ObjectDoesNotExist:
            return Response({'error': 'Product variant does not exists.'}, status=404)
        except ValidationError as e:
            return Response({'error': str(e)}, status=400)

        serializer = CartItemSerializer(result.cart_item)
        out_code = cart_code or result.cart_code 
        return Response({
            'cart_code': out_code,
            'data': serializer.data,
            'message': 'Cart item created successfully.'
        }, status=201)

    @action(detail=True, methods=['get'], url_path='num_of_items')
    def get_num_of_items(self, request, pk=None):
        svc = self.service_class()
        if not pk:
            return Response({'error': 'Cart code is required.'}, status=400)
        try:
            cart = svc.get_summary_cart(pk)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart does not exists.'}, status=404)
        return Response(CartNumItemsSerializer(cart).data)

    def retrieve(self, request, pk=None):
        svc = self.service_class()
        try:
            cart = svc.get_detail_cart(pk)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart does not exists.'}, status=404)
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=['patch'], url_path=r'(?P<cart_code>[0-9A-Za-z\-]+)/item/(?P<item_id>\d+)/update_quantity')
    def update_cart_items_quantity(self, request, cart_code=None, item_id=None):
        svc = self.service_class()
        try:
            quantity = int(request.data.get('quantity'))
            item = svc.update_item_quantity(cart_code, item_id, quantity)
            return Response({'data': CartItemSerializer(item).data, 'message': 'Cart item updated successfully.'}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    @action(detail=False, methods=['delete'], url_path=r'(?P<cart_code>[0-9A-Za-z\-]+)/item/(?P<item_id>\d+)/delete')
    def delete_cart_item(self, request, cart_code=None, item_id=None):
        svc = self.service_class()
        try:
            svc.delete_item(cart_code, item_id)
            return Response({'message': 'Cart item deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
