from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from apps.payments.models import PaymentMethod
from apps.common.consts.payments_consts import PaymentProvider
from django.db import transaction

class PaymentService:
    def get_list_of_payment_methods(self):
        return PaymentMethod.objects.filter(is_active=True)