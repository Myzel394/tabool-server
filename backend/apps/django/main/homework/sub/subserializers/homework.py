from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.django.utils.serializers import (
    PreferredIdsMixin, RandomIDSerializerMixin, UserRelationField,
    WritableSerializerMethodField,
)
from .user_relations import UserHomeworkRelationSerializer
from ...models import Homework


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
        deserializer_field=serializers.BooleanField()
    )
    
    user_relation = UserRelationField(UserHomeworkRelationSerializer)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_private = False
    
    @staticmethod
    def get_is_private(obj: Homework):
        return obj.is_private
    
    def set_is_private(self, value: bool):
        self._is_private = value
    
    def create(self, validated_data):
        validated_data["private_to_user"] = self.context["request"].user if self._is_private else None
        
        return super().create(validated_data)
    
    def validate(self, attrs):
        if self.instance and not self.instance.is_private and self._is_private:
            raise ValidationError({
                "is_private": _("Öffentliche Hausaufgaben können nicht privat gestellt werden.")
            })
        
        return super().validate(attrs)
