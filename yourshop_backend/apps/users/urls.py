from rest_framework.routers import DefaultRouter
from apps.users.views.user_viewset import UserViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    *router.urls,
]
