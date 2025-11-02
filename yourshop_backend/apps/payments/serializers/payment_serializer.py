from rest_framework import serializers
from apps.payments.models import PaymentMethod

class PaymentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            'id', 'code', 'name', 'provider', 'fee_flat', 'fee_percent', 'created_at', 'modified_at'
        ]
        read_only_fields = [
            'id', 'code', 'name', 'provider'
        ]