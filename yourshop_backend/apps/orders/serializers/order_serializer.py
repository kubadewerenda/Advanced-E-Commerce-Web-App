from rest_framework import serializers
from apps.orders.models import Order, OrderItem, PaymentMethod
from apps.shipping.models import DeliveryMethod
from apps.common.consts.shipping_consts import AddressType
import re

POSTAL_PL_RGX = re.compile(r'^\d{2}-\d{3}$')
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'variant_id', 'product_name', 'sku', 'quantity', 'unit_price', 'line_total']
        read_only_fields = ['id', 'line_total']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id','status','payment_status','currency', 'address_type',
            'first_name','last_name','company_name','tax_number',
            'street','house_number','apartament_number','postal_code',
            'city','country','phone','email',
            'subtotal_amount','shipping_amount','discount_amount','total_amount',
            'payment_fee_amount', 'items','created_at','modified_at'
        ]
        read_only_fields = [
            'id','status','payment_status','subtotal_amount','shipping_amount',
            'discount_amount','total_amount','created_at','modified_at',
            'payment_fee_amount',
        ]

class OrderCheckoutSerializer(serializers.Serializer):
    cart_code = serializers.CharField(required=False, allow_blank=False)

    address_id = serializers.IntegerField(required=False)

    delivery_method_id = serializers.IntegerField(required=True)
    payment_method_id = serializers.IntegerField(required=True)

    address_type = serializers.CharField(required=False, max_length=16)
    first_name = serializers.CharField(required=False, max_length=50)
    last_name = serializers.CharField(required=False, max_length=80, allow_blank=True)
    company_name = serializers.CharField(required=False, max_length=500, allow_blank=True)
    tax_number = serializers.CharField(required=False, max_length=64, allow_blank=True)
    street = serializers.CharField(required=False, max_length=255)
    house_number = serializers.CharField(required=False, max_length=30)
    apartament_number = serializers.CharField(required=False, max_length=30, allow_blank=True)
    postal_code = serializers.CharField(required=False, max_length=30)
    city = serializers.CharField(required=False, max_length=150)
    country = serializers.CharField(required=False, max_length=100, default='Polska')
    phone = serializers.CharField(required=False, max_length=30, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    def validate(self, attrs):
        user = self.context['request'].user

        if not user.is_authenticated and not attrs.get('cart_code'):
            raise serializers.ValidationError({'cart_code': 'Required for guest checkout.'})

        dm = DeliveryMethod.objects.filter(id=attrs.get('delivery_method_id'), is_active=True).first()
        pm = PaymentMethod.objects.filter(id=attrs.get('payment_method_id'), is_active=True).first()
        if not dm:
            raise serializers.ValidationError({'delivery_method_id': 'Invalid delivery method.'})
        if not pm:
            raise serializers.ValidationError({'payment_method_id': 'Invalid payment method.'})

        if user.is_authenticated and attrs.get('address_id'):
            return attrs

        required = [
            'address_type', 'first_name', 'street',
            'house_number', 'postal_code', 'city',
            'country', 'email'
        ]
        missing = [f for f in required if not attrs.get(f)]
        if missing:
            raise serializers.ValidationError({'shipping': f'Missing fields: {", ".join(missing)}'})

        if attrs.get('address_type') == AddressType.COMPANY:
            if not attrs.get('company_name'):
                raise serializers.ValidationError({'company_name': 'Company name is required.'})
            if not attrs.get('tax_number'):
                raise serializers.ValidationError({'tax_number': 'Tax number is required.'})

        p_code = attrs.get('postal_code')
        if not POSTAL_PL_RGX.match(p_code):
            raise serializers.ValidationError({'postal_code': 'Format must be XX-XXX.'})

        return attrs