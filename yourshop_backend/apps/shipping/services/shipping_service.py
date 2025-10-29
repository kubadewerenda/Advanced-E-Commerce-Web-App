from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from apps.shipping.models import ShippingAddress
from django.db import transaction

class ShippingAddressService:
    def get_shipping_addresses(self, user):
        return (ShippingAddress.objects
                .filter(user=user, is_active=True)
                .select_related('user'))
    
    def create_shipping_address(self, user, data: dict) -> ShippingAddress:
        if data.get('is_default'):
            ShippingAddress.objects.filter(user=user, is_default=True, is_active=True).update(is_default=False)

        address = ShippingAddress(user=user, **data)
        address.full_clean()
        address.save()

        return address
    
    def update_shipping_address(self, user, data: dict, pk: int = None) -> ShippingAddress:
        address = ShippingAddress.objects.get(pk=pk, is_active=True)

        if not address:
            raise ObjectDoesNotExist('There is no such address.')
        if address.user.id != user.id:
            raise PermissionDenied('This is not your address.')
        
        for k, v in data.items():
            setattr(address, k, v)
        
        address.full_clean()
        address.save()

        return address
    
    def delete_shipping_address(self, user, pk=None) -> None:
        address = ShippingAddress.objects.get(pk=pk, is_active=True)#filter == QuerySet
        if not address:
            raise ObjectDoesNotExist('There is no such address')
        if address.user.id != user.id:
            raise PermissionDenied('This is not your address.')
        
        address.is_active = False
        address.save()

    @transaction.atomic
    def set_default_shipping_address(self, user, pk=None) -> ShippingAddress:
        address = ShippingAddress.objects.get(pk=pk, user=user, is_active=True)
        ShippingAddress.objects.filter(user=user, is_default=True, is_active=True).exclude(pk=address.pk).update(is_default=False) 

        if not address:
            raise ObjectDoesNotExist('There is not such address.')
        if address.user.id != user.id:
            raise PermissionDenied('This is not your address.')
        
        address.is_default = True
        address.full_clean()
        address.save()

        return address
