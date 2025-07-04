from django.db import models
from django.utils.text import slugify
import uuid
from django.conf import settings
import string
import random

# Create your models here.
class Cart(models.Model):
    cart_code = models.CharField(max_length=15, unique=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="carts",
        null=True,
        blank=True
    )
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def generate_cart_code(length=10):
        chars = string.ascii_uppercase + string.digits
        return "CART-" + "".join(random.choices(chars, k=length))
    
    def save(self, *args, **kwargs):
        if not self.cart_code:
            while True:
                code = self.generate_cart_code()
                if not Cart.objects.filter(cart_code=code).exists():
                    self.cart_code=code
                    break
        super().save(*args, **kwargs)
    
    def __str__(self):
        if self.user:
            return f"{self.user.email} -> {self.cart_code}"
        return self.cart_code

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    variant = models.ForeignKey("shop_app.ProductVariant", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.variant} in cart {self.cart}"