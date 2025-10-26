from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Lower
from django.core.validators import MaxValueValidator, MinValueValidator
from .base_model import BaseModel

class CustomUser(AbstractUser, BaseModel):
    email = models.EmailField('email address', unique=True, db_index=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    phone_number = models.CharField(max_length=20, blank=True)
    is_company = models.BooleanField(default=False)
    company_name = models.CharField(max_length=255, blank=True)
    tax_number = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)

    discount_percent = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

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

    def __str__(self):
        return f'{self.email} ({self.first_name} {self.last_name})'
