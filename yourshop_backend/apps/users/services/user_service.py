from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError

from apps.users.serializers.user_serializer import UserUpdateSerializer

User = get_user_model()

class UserService:
    def register(self, data):
        return data
    
    def authenticate_user(self, *, request=None, email: str, password: str):
        user = authenticate(username=email, password=password)
        if not user:
            raise ValidationError('Wrong email or password.')
        if not user.is_active:
            raise ValidationError('This account is no longer active.')
        return user
    
    def issue_tokens(self, user) -> RefreshToken:
        return RefreshToken.for_user(user)
    
    def rotate_refresh(self, raw_refresh: str) -> RefreshToken:
        if not raw_refresh:
            raise ValidationError('There is no refresh token.')
        old = RefreshToken(raw_refresh)
        try:
            old.blacklist()
        except Exception:
            pass
        user_id = old['user_id']
        user = User.objects.get(id=user_id)
        return RefreshToken.for_user(user)
    
    def blacklist_refresh(self, raw_refresh: str):
        if not raw_refresh:
            raise
        try:
            RefreshToken(raw_refresh).blacklist()
        except Exception:
            pass
    
    def get_me(self, user):
        if not user or not user.is_authenticated:
            raise ValidationError('User is not signed in.')
        return user
    
    def update_me(self, user, data):
        if not user or not user.is_authenticated:
            raise ValidationError('User is not signed in.')
        serializer = UserUpdateSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.instance