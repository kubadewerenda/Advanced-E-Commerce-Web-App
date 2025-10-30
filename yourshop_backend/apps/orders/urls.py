from rest_framework.routers import DefaultRouter
from apps.orders.views.order_viewset import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    *router.urls,
]