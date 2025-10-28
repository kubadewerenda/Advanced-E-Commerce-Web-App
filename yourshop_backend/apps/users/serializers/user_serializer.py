from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'phone_number',
            'is_company', 'company_name', 'tax_number', 'address', 'postal_code',
            'city', 'discount_percent'
        ]
        read_only_fields = [
            'id', 'discount_percent'
        ]
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "phone_number",
            "is_company", "company_name", "tax_number",
            "address", "postal_code", "city",
        ]

    def validate(self, attrs):
        for k, v in list(attrs.items()):
            if isinstance(v, str):
                vv = v.strip()
                attrs[k] = vv or v 
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    password2 = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2']

    def validate_email(self, v):
        if User.objects.filter(email__iexact=v).exists():
            raise serializers.ValidationError('Account with this email already exists.')
        return v
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Both passwords must be the same.'})
        password_validation.validate_password(data['password'])
        return data
    
    def create(self, validated_data):
        pwd = validated_data.pop('password')
        validated_data.pop('password2', None)
        user = User(**validated_data)
        user.set_password(pwd)
        user.save()
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)