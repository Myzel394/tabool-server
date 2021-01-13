from typing import *

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.django.utils.serializers import (
    PreferredIdsMixin, RandomIDSerializerMixin, UserRelationField,
    WritableSerializerMethodField,
)
from .user_relations import UserHomeworkRelationSerializer
from ...models import Homework

if TYPE_CHECKING:
    from apps.django.main.authentication.models import User


class HomeworkDetailSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "homework"
    instance: Homework
    
    class Meta:
        model = Homework
        fields = [
            "is_private", "due_date", "information", "type", "created_at", "id", "user_relation"
        ]
        read_only_fields = [
            "created_at", "id", "user_relation"
        ]
    
    is_private = WritableSerializerMethodField(
        deserializer_field=serializers.BooleanField(allow_null=True)
    )
    
    user_relation = UserRelationField(
        UserHomeworkRelationSerializer,
        default={
            "completed": False,
            "ignore": False
        }
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
    
    def update(self, instance, validated_data):
        validated_data["private_to_user"] = self.get_private_to_user()
        
        return super().update(instance, validated_data)
    
    def create(self, validated_data):
        validated_data["private_to_user"] = self.get_private_to_user()
        
        return super().create(validated_data)
    
    def validate(self, attrs):
        if self.instance and not self.instance.is_private and self._is_private:
            raise ValidationError({
                "is_private": _("Öffentliche Hausaufgaben können nicht privat gestellt werden.")
            })
        
        return super().validate(attrs)
