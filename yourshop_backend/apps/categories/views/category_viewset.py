from rest_framework import viewsets, permissions
from rest_framework.response import Response
from apps.categories.serializers.category_serializer import CategorySerializer
from apps.categories.services.category_service import CategoryService

class CategoryViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    service_class = CategoryService

    def list(self, request):
        svc = self.service_class()
        categories = svc.get_categories()
        return Response(CategorySerializer(categories, many=True, context={'request': request, 'view': self}).data)