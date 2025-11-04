from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate

from apps.users.serializers.user_serializer import UserSerializer, RegisterSerializer
from apps.users.services.user_service import UserService

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
    service_class = UserService

    @method_decorator(ensure_csrf_cookie)
    @action(detail=False, methods=['get'], url_path='csrf')
    def csrf(self, request):
        return Response({'message': 'CSRF cookie set.'})
    
    @action(detail=False, methods=['post'], url_path='refresh')
    def refresh(self, request):
        svc = self.service_class()
        raw = request.COOKIES.get(REFRESH_COOKIE)
        try:
            new_refresh = svc.rotate_refresh(raw)
            res = Response({'message': 'Token refreshed'}, status=200)
            return set_jwt_cookies(res, new_refresh)
        except (InvalidToken, TokenError):
            return Response({'error': 'Invalid refresh token.'}, status=401)
        
    
    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        svc = self.service_class()
        reg = RegisterSerializer(data=request.data)
        reg.is_valid(raise_exception=True)
        user = reg.save()
        refresh = svc.issue_tokens(user) #autologin
        res = Response({'user': UserSerializer(user).data, 'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)
        return set_jwt_cookies(res, refresh)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        svc = self.service_class()
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=401)
        try:
            user = svc.authenticate_user(request=request, email=email, password=password)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
        refresh = svc.issue_tokens(user)
        res = Response({'user': UserSerializer(user).data, 'message': 'User signed in successfully.'}, status=200)
        return set_jwt_cookies(res, refresh)

    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        svc = self.service_class()
        raw = request.COOKIES.get(REFRESH_COOKIE)
        svc.blacklist_refresh(raw)
        res = Response({'message': 'Logged out successfully.'}, status=status.HTTP_204_NO_CONTENT)
        return clear_jwt_cookies(res)
    
    @action(detail=False, methods=['get'], url_path='me', permission_classes=[IsAuthenticated])
    def me(self, request):
        svc =self.service_class()
        if not request.user:
            return Response({'error': 'User does not exists.'}, status=404)
        try:
            user = svc.get_me(request.user)
        except Exception as e:
            return Response({'error': str(e)}, status=401)

        return Response(UserSerializer(user).data)
    
    @action(detail=False, methods=['patch'], url_path='update_me', permission_classes=[IsAuthenticated])
    def update_me(self, request):
        svc = self.service_class()
        if not request.user:
            return Response({'error': 'User does not exists'})
        try:
            user = svc.update_me(request.user, request.data)
        except Exception as e:
            return Response({'error': str(e)})
        return Response(UserSerializer(user).data)
    

    
# --- TODO: ----
# 1. Dodać weryfikacje maila przy rejestracji
# 2. Dodać oautha od google
# 3. dodac zaleznosci, jaka firma tyle znizek itp(typ firmy np. masarnia)

