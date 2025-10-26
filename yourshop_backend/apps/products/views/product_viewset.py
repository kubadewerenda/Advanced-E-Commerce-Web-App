from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.products.models import Product
from apps.products.serializers.product_serializer import ProductSerializer, DetailedProductSerializer
from apps.products.services.product_service import ProductService
from apps.products.pagination.product_pagination import QueryPageNumberPagination 

class ProductViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    service_class = ProductService
    pagination_class = QueryPageNumberPagination

    def list(self, request):
        svc = self.service_class()
        qs, min_price_map = svc.get_product_list(request.query_params)

        paginator = self.pagination_class()
        paginated_qs = paginator.paginate_queryset(qs, request)
        serializer = ProductSerializer(paginated_qs, many=True, context={'min_price_map': min_price_map})
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        svc = self.service_class()
        try:
            product = svc.get_product_detail(pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DetailedProductSerializer(product)
        return Response(serializer.data)