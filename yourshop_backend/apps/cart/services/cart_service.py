from dataclasses import dataclass
from typing import Optional
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from apps.cart.models import Cart, CartItem
from apps.products.models import ProductVariant


@dataclass
class AddToCartResult:
    cart_code: str
    cart_item: CartItem
    created: bool


class CartService:
    def _get_or_create_cart(self, user, cart_code: Optional[str]) -> Cart:
        if user.is_authenticated:
            cart = Cart.objects.filter(user=user, paid=False).first()
            if not cart:
                return Cart.objects.create(user=user)
            else:
                return cart
        # guest cart, if not signed in
        if cart_code:
            cart = Cart.objects.filter(cart_code=cart_code, paid=False).first()
            if not cart:
                return Cart.objects.create()
            else:
                return cart
        # return cart anyway if not returned earlier
        return Cart.objects.create()

    def add_item(self, user, cart_code: Optional[str], variant_sku: str, quantity: int) -> AddToCartResult:
        if not variant_sku:
            raise ValidationError('Missing variant SKU.')

        try:
            variant = ProductVariant.objects.get(sku=variant_sku)
        except ProductVariant.DoesNotExist:
            raise ObjectDoesNotExist('Variant not found.')

        cart = self._get_or_create_cart(user, cart_code)

        item, created = CartItem.objects.get_or_create(cart=cart, variant=variant)
        if created:
            item.quantity = int(quantity or 1)
        else:
            item.quantity += int(quantity or 1)
        item.save()

        return AddToCartResult(cart_code=cart.cart_code, cart_item=item, created=created)

    def get_summary_cart(self, cart_code: str) -> Cart:
        return Cart.objects.get(cart_code=cart_code, paid=False)

    def get_detail_cart(self, cart_code: str) -> Cart:
        return Cart.objects.get(cart_code=cart_code, paid=False)

    def update_item_quantity(self, item_id: int, quantity: int) -> CartItem:
        if quantity is None:
            raise ValidationError('Missing quantity.')
        item = CartItem.objects.get(id=item_id)
        if quantity <= item.variant.stock:
            item.quantity = int(quantity)
        else:
            raise ValidationError('Quantity of this item is overstock.')
        item.save()
        return item

    def delete_item(self, item_id: int) -> None:
        item = CartItem.objects.get(id=item_id)
        item.delete()
