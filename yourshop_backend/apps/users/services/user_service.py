from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class UserService:
    def register(self, data):
        raise NotImplementedError
    
    def authenticate_user(self, request, *, email: str, password: str):
        user = authenticate(request, username=email, password=password)
        return user