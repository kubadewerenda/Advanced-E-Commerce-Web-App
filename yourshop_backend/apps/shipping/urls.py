from rest_framework.routers import DefaultRouter
from apps.shipping.views.shipping_viewset import ShippingAddressViewSet

router = DefaultRouter()
router.register(r'users/shipping_addresses', ShippingAddressViewSet, basename='users/shipping_addresses')

urlpatterns = [
    *router.urls,
]
