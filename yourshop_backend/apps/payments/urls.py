from rest_framework.routers import DefaultRouter
from apps.payments.views.payment_viewset import PaymentViewSet
router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = [
    *router.urls,
]