from rest_framework.routers import DefaultRouter
from apps.cart.views.cart_view import CartViewSet

router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    *router.urls,
]