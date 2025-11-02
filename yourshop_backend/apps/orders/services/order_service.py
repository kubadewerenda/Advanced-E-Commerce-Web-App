from decimal import Decimal
from django.db import transaction
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from apps.orders.models import Order, OrderItem, PaymentMethod
from apps.common.consts.payments_consts import PaymentStatus
from apps.common.consts.orders_consts import OrderStatus
from apps.cart.models.cart import Cart
from apps.cart.models.cart_item import CartItem
from apps.products.models.product_variant import ProductVariant
from apps.shipping.models import ShippingAddress, DeliveryMethod

from typing import Optional
from django.db.models import QuerySet

CENT = Decimal('0.01')


class OrderService:
    def _get_cart_for_request(self, user, cart_code: Optional[str]) -> Cart:
        if user.is_authenticated:
            cart = None

            if cart_code:
                cart = Cart.objects.filter(cart_code=cart_code, paid=False).first()
                if not cart:
                    raise NotFound('Cart not found.')

                if cart.user_id and cart.user_id != user.id:
                    raise PermissionDenied('This cart does not belong to you.')

                if not cart.user_id:
                    cart.user = user
                    cart.save(update_fields=['user'])

            if not cart:
                cart = (Cart.objects
                        .filter(user=user, paid=False)
                        .order_by('-created_at')
                        .first())
            if not cart:
                raise NotFound('Active cart not found.')
            return cart

        if not cart_code:
            raise ValidationError({'cart_code': 'Required for guest checkout.'})

        cart = (Cart.objects
                .filter(cart_code=cart_code, paid=False, user__isnull=True)
                .first())
        if not cart:
            owned = Cart.objects.filter(cart_code=cart_code, paid=False, user__isnull=False).exists()
            if owned:
                raise PermissionDenied('This cart belongs to a user account. Please log in.')
            raise NotFound('Cart not found.')
        return cart

    def _get_shipping_snapshot_from_address(self, addr: ShippingAddress) -> dict:
        return {
            'address_type': addr.address_type,
            'first_name': addr.first_name,
            'last_name': addr.last_name,
            'company_name': addr.company_name,   
            'tax_number': addr.tax_number,        
            'street': addr.street,
            'house_number': addr.house_number,
            'apartament_number': addr.apartament_number,
            'postal_code': addr.postal_code,    
            'city': addr.city,
            'country': addr.country,
            'phone': addr.phone,
            'email': addr.email or '',
        }

    def _get_shipping_snapshot_from_payload(self, data: dict) -> dict:
        keys = [
            'address_type', 'first_name', 'last_name', 'company_name', 'tax_number',
            'street', 'house_number', 'apartament_number', 'postal_code',
            'city', 'country', 'phone', 'email'
        ]
        return {k: data.get(k, '') for k in keys}

    def _unit_price_for_variant(self, variant: ProductVariant) -> Decimal:
        return variant.discount_price if variant.discount_price is not None else variant.price

    def _calc_discounts(self, user, subtotal: Decimal) -> Decimal:
        return Decimal('0.00')

    def get_orders_for_user(self, user) -> QuerySet[Order]:
        if user.is_authenticated:
            return Order.objects.filter(user=user).prefetch_related('items')

    def get_order_for_user(self, user, pk: Optional[int] = None) -> Optional[Order]:
        return Order.objects.filter(pk=pk, user=user).prefetch_related('items').first()

    @transaction.atomic
    def create_from_cart(self, request_user, payload: dict) -> Order:
        cart = self._get_cart_for_request(request_user, payload.get('cart_code'))

        items = (CartItem.objects
                    .select_related('variant', 'variant__product')
                    .select_for_update()
                    .filter(cart=cart))
        if not items.exists():
            raise ValidationError('Cart is empty.')

        if getattr(request_user, "is_authenticated", False) and payload.get('address_id'):
            address = (
                ShippingAddress.objects
                    .filter(id=payload['address_id'], user=request_user, is_active=True)
                    .first()
            )
            if not address:
                raise NotFound('Shipping address not found.')
            shipping = self._get_shipping_snapshot_from_address(address)
        else:
            shipping = self._get_shipping_snapshot_from_payload(payload)

        dm = DeliveryMethod.objects.get(id=payload['delivery_method_id'], is_active=True)
        pm = PaymentMethod.objects.get(id=payload['payment_method_id'], is_active=True)

        order = Order.objects.create(
            user=request_user if getattr(request_user, "is_authenticated", False) else None,
            delivery_method=dm,
            payment_method=pm,
            status=OrderStatus.PENDING,
            payment_status=PaymentStatus.NOT_PAID,
            currency='PLN',
            **shipping
        )

        subtotal = Decimal('0.00')
        to_create = []

        for ci in items:
            v = ci.variant
            if not v.is_active or v.stock <= 0 or ci.quantity > v.stock:
                raise ValidationError(f'Variant {v.sku} is not available in requested quantity.')

            unit_price = self._unit_price_for_variant(v)  # Decimal
            line_total = (unit_price * ci.quantity).quantize(CENT)
            subtotal = (subtotal + line_total).quantize(CENT)

            to_create.append(OrderItem(
                order=order,
                product_id=v.product_id,        
                variant_id=v.id,
                product_name=f'{v.product.name} | {v.name or ""}'.strip(),
                sku=v.sku or '',
                quantity=ci.quantity,
                unit_price=unit_price,
                line_total=line_total,
            ))

        OrderItem.objects.bulk_create(to_create)

        # Including delivery price, or if free, then free
        if dm.free_from is not None and subtotal >= dm.free_from:
            shipping_amount = Decimal('0.00')
        else: 
            shipping_amount = dm.fixed_price.quantize(CENT)

        discount_amount = self._calc_discounts(request_user, subtotal).quantize(CENT)

        tmp_total = (subtotal + shipping_amount - discount_amount).quantize(CENT)

        fee_percent = (pm.fee_percent or Decimal('0')) / Decimal('100')
        payment_fee_amonut = (tmp_total * fee_percent + (pm.fee_flat or Decimal('0'))).quantize(CENT)

        total = (tmp_total + payment_fee_amonut)

        order.subtotal_amount = subtotal
        order.shipping_amount = shipping_amount
        order.discount_amount = discount_amount
        order.total_amount = total
        order.save()

        items.delete()

        return order
