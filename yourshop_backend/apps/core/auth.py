from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication

ACCESS_COOKIE = getattr(settings, "JWT_ACCESS_COOKIE_NAME", "access_token")

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is not None:
            raw_token = self.get_raw_token(header)
        else:
            raw_token = request.COOKIES.get(ACCESS_COOKIE)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
