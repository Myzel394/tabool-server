from typing import Optional

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.django.main.homework.models import Homework
from apps.django.utils.serializers import WritableSerializerMethodField

__all__ = [
    "IsPrivateMixin"
]


class IsPrivateMixin:
    is_private = WritableSerializerMethodField(
        deserializer_field=serializers.BooleanField(allow_null=True)
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_private = None
    
    def get_private_to_user(self) -> Optional["User"]:
        user = None
        
        if self._is_private == True:
            user = self.context["request"].user
        elif self._is_private == False:
            user = None
        else:
            if self.instance:
                user = self.instance.private_to_user
        
        return user
    
    @staticmethod
    def get_is_private(obj: Homework):
        return obj.is_private
    
    def set_is_private(self, value: bool):
        self._is_private = value
    
    def validate(self, attrs):
        if self.instance and not self.instance.is_private and self._is_private:
            raise ValidationError({
                "is_private": _("Öffentliche Hausaufgaben können nicht privat gestellt werden.")
            })
        
        return super().validate(attrs)
