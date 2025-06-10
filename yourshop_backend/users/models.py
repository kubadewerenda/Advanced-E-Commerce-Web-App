from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField("email address", unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    phone_number = models.CharField(max_length=20, blank=True)
    is_company = models.BooleanField(default=False)
    company_name = models.CharField(max_length=255, blank=True)
    tax_number = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)

    discount_percent = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return f"{self.email} ({self.first_name} {self.last_name})"
