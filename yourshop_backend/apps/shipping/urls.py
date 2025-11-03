from rest_framework.routers import DefaultRouter
from apps.shipping.views.address_viewset import ShippingAddressViewSet
from apps.shipping.views.delivery_viewset import DeliveryViewSet

router = DefaultRouter()
router.register(r'shipping/user/addresses', ShippingAddressViewSet, basename='shipping/user/addresses')
router.register(r'shipping/delivery_methods', DeliveryViewSet, basename='shipping/delivery_methods')

urlpatterns = [
    *router.urls,
]
