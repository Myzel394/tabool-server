from datetime import datetime

from rest_framework import serializers

from apps.utils.serializers import WritableSerializerMethodField
from ...models import UserPayment
from ...public.serializer_fields import UserField

__all__ = [
    "UserPaymentDetailSerializer", "ManageUserPaymentSerializer"
]


class UserPaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPayment
        fields = [
            "user", "paid_at", "id"
        ]
    
    user = UserField()


class ManageUserPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPayment
        fields = [
            "user", "has_paid", "id"
        ]
    
    user = UserField()

    has_paid = WritableSerializerMethodField(
        deserializer_field=serializers.BooleanField()
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._has_paid = False
    
    @staticmethod
    def get_has_paid(instance: UserPayment):
        return instance.has_paid
    
    def set_has_paid(self, value):
        self._has_paid = value
    
    def update(self, instance, validated_data):
        instance.paid_at = datetime.now() if self._has_paid else None
        instance.save()
        return instance
        
        
        
        
        
        

