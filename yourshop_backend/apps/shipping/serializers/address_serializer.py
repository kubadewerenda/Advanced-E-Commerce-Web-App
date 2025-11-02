from rest_framework import serializers
import re

from apps.shipping.models import ShippingAddress
from apps.common.consts.shipping_consts import AddressType
from apps.common.utils import get_instance_value

POSTAL_PL_RGX = re.compile(r'^\d{2}-\d{3}$')

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = [
            'id', 'user', 'address_type', 'first_name', 'last_name', 'company_name',
            'tax_number', 'street', 'house_number', 'apartament_number', 'postal_code', 'city', 'country',
            'phone', 'email', 'is_default', 'is_active', 'created_at', 'modified_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'modified_at']

    def validate(self, attrs):
        instance = getattr(self, 'instance', None)
        
        if get_instance_value(instance, attrs, 'address_type') == AddressType.COMPANY:
            if not get_instance_value(instance, attrs, 'company_name', ''):
                raise serializers.ValidationError('Company name is required for company address.')
            if not get_instance_value(instance, attrs, 'tax_number', ''):
                raise serializers.ValidationError('Tax number is required for company address.')
        p_code = get_instance_value(instance, attrs, 'postal_code', '')
        if not p_code or not  POSTAL_PL_RGX.match(p_code):
            raise serializers.ValidationError('Postal code is required with format NN-NNN.')
        return attrs