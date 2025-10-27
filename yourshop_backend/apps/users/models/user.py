from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.functions import Lower
from django.core.validators import MaxValueValidator, MinValueValidator
from .base_model import BaseModel

class UserRole(models.TextChoices):
    USER = 'user', 'User'
    ADMIN = 'admin', 'Admin'

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        if 'role' not in extra_fields:
            user.role = UserRole.USER
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', UserRole.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not password:
            raise ValueError('Superuser must have a password.')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField('email address', unique=True, db_index=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20, blank=True)

    cart_code = models.CharField(max_length=20, blank=True, null=True)

    is_company = models.BooleanField(default=False)
    company_name = models.CharField(max_length=255, blank=True)
    tax_number = models.CharField(max_length=30, blank=True)

    address = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)

    role = models.CharField(
        max_length=16,
        choices=UserRole.choices,
        default=UserRole.USER,
        db_index=True
    )

    discount_percent = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(Lower('email'), name='users_email_ci_idx'),
        ]
        constraints = [
            models.UniqueConstraint(
                Lower('email'),
                name='users_email_ci_unique'
            ),
        ]

    @property
    def is_user_admin(self):
        return self.role == UserRole.ADMIN

    def save(self, *args, **kwargs):
        if self.role == UserRole.ADMIN:
            self.is_staff = True
        else:
            self.is_staff = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.email} ({self.first_name} {self.last_name})'
