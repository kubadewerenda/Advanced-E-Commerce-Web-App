from rest_framework.routers import DefaultRouter
from apps.users.views.user_viewset import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    *router.urls,
]
