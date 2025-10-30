from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.shipping.models import DeliveryMethod

class DeliveryViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        qs = DeliveryMethod.objects.filter(is_active=True)
        data = [{
            'id': d.id,
            'code': d.code, 
            'name': d.name, 
            'price': str(d.fixed_price),
            'free_from': str(d.free_from) if d.free_from is not None else None
        } for d in qs]

        return Response(data)
    
    # --- TODO: ---
    # 1. Zrobic dodawanie, updatowanie, usowanie dla admina
    
    # @action(detail=False, methods=['post'],url_path='create', permission_classes = [permissions.IsAuthenticated])
    # def create_delivery(self, request):