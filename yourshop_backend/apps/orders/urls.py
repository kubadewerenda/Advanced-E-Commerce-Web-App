from rest_framework.routers import DefaultRouter
from apps.orders.views.order_viewset import OrderViewSet

router = DefaultRouter()
router.register(r'user/orders', OrderViewSet, basename='user/orders')

urlpatterns = [
    *router.urls,
]