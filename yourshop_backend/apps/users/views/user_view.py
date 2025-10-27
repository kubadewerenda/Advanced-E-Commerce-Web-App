from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate

from apps.users.serializers.user_serializer import UserSerializer, RegisterSerializer

ACCESS_COOKIE = getattr(settings, "JWT_ACCESS_COOKIE_NAME", "access_token")
REFRESH_COOKIE = getattr(settings, "JWT_REFRESH_COOKIE_NAME", "refresh_token")
COOKIE_SECURE = getattr(settings, "JWT_COOKIE_SECURE", True)
COOKIE_SAMESITE = getattr(settings, "JWT_COOKIE_SAMESITE", "Lax")
COOKIE_DOMAIN = getattr(settings, "JWT_COOKIE_DOMAIN", None)

def set_jwt_cookies(response, refresh: RefreshToken):
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    access_max_age = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
    refresh_max_age = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())

    response.set_cookie(
        key=ACCESS_COOKIE, value=access_token, max_age=access_max_age,
        httponly=True, secure=COOKIE_SECURE, samesite=COOKIE_SAMESITE,
        domain=COOKIE_DOMAIN, path="/",
    )
    response.set_cookie(
        key=REFRESH_COOKIE, value=refresh_token, max_age=refresh_max_age,
        httponly=True, secure=COOKIE_SECURE, samesite=COOKIE_SAMESITE,
        domain=COOKIE_DOMAIN, path="/",
    )
    return response

def clear_jwt_cookies(response):
    response.delete_cookie(ACCESS_COOKIE, path="/", domain=COOKIE_DOMAIN, samesite=COOKIE_SAMESITE)
    response.delete_cookie(REFRESH_COOKIE, path="/", domain=COOKIE_DOMAIN, samesite=COOKIE_SAMESITE)
    return response

class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @method_decorator(ensure_csrf_cookie)
    @action(detail=False, methods=['get'], url_path='csrf')
    def csrf(self, request):
        return Response({'message': 'CSRF cookie set.'})