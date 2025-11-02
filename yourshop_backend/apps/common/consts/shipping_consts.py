from django.db import models

class AddressType(models.TextChoices):
    PERSONAL = 'personal', 'Personal'
    COMPANY = 'company', 'Company'