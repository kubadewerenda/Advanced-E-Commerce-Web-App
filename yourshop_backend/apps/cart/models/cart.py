from django.db import models
from django.conf import settings
import string
import random
from .base_model import BaseModel

class Cart(BaseModel):
    cart_code = models.CharField(max_length=15, unique=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carts',
        null=True,
        blank=True
    )
    paid = models.BooleanField(default=False)

    class Meta:
        db_table = 'carts'
        ordering = ['-created_at']

    @staticmethod
    def generate_cart_code(length=10):
        chars = string.ascii_uppercase + string.digits
        return 'CART-' + ''.join(random.choices(chars, k=length))
    
    def save(self, *args, **kwargs):
        if not self.cart_code:
            while True:
                code = self.generate_cart_code()
                if not Cart.objects.filter(cart_code=code).exists():
                    self.cart_code = code
                    break
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.user.email} -> {self.cart_code}' if self.user else self.cart_code
