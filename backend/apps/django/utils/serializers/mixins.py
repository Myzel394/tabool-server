from abc import abstractmethod
from typing import *

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from simple_history.models import ModelChange, ModelDelta

from apps.django.utils.serializers import HistoryUserField
from apps.utils.files import privatize_file

__all__ = [
    "RandomIDSerializerMixin", "AssociatedUserSerializerMixin",
    "PrivatizeSerializerMixin", "GetOrCreateSerializerMixin", "ModelHistoryListSerializerMixin",
    "ModelHistoryDetailSerializerMixin"
]


class RandomIDSerializerMixin(serializers.ModelSerializer):
    id = serializers.CharField(
        read_only=True
    )


class AssociatedUserSerializerMixin(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        validated_data.pop("associated_user", None)
        return super().update(instance, validated_data)
    
    def create(self, validated_data):
        validated_data["associated_user"] = self.context["request"].user
        return super().create(validated_data)


M = TypeVar("M")
S = TypeVar("S")


class PrivatizeSerializerMixin(serializers.ModelSerializer):
    privatize = serializers.BooleanField(
        label=_("Private Daten entfernen"),
        help_text=_("Entfernt private Daten und verschleiert Daten, die nicht entfernt werden können."),
        write_only=True,
        default=True
    )
    
    @abstractmethod
    def get_file_to_privatize(self, instance, validated_data: Dict[str, Any]) -> List[str]:
        raise NotImplementedError()
    
    def create(self, validated_data):
        should_privatize = validated_data.pop("privatize", True)
        
        instance = super().create(validated_data)
        
        if should_privatize:
            for file in self.get_file_to_privatize(instance, validated_data):
                privatize_file(file)
        return instance
    
    def update(self, instance, validated_data):
        should_privatize = validated_data.pop("privatize", True)
        
        instance = super().update(instance, validated_data)
        
        if should_privatize:
            for file in self.get_file_to_privatize(instance, validated_data):
                privatize_file(file)
        return instance


class GetOrCreateSerializerMixin(serializers.ModelSerializer):
    def get_unique_fields(self, validated_data):
        return validated_data
    
    def create(self, validated_data):
        unique_data = self.get_unique_fields(validated_data)
        
        instance = self.Meta.model.objects.get_or_create(**unique_data)[0]
        self.update(instance, validated_data)
        
        return instance


class ModelHistoryListSerializerMixin(serializers.ModelSerializer):
    class Meta:
        fields = ["history_date", "history_user", "changes", "pk"]
    
    history_date = serializers.DateTimeField()
    history_user = HistoryUserField()
    changes = serializers.SerializerMethodField()
    
    def get_changes(self, instance) -> list[str]:
        delta: ModelDelta = self.context["latest_history_instance"].diff_against(instance)
        
        return delta.changed_fields


class ModelHistoryDetailSerializerMixin(serializers.ModelSerializer):
    class Meta:
        fields = ["history_date", "history_user", "changes", "pk"]
    
    history_date = serializers.DateTimeField()
    history_user = HistoryUserField()
    changes = serializers.SerializerMethodField()
    
    def get_changes(self, instance) -> dict:
        delta: ModelDelta = self.context["latest_history_instance"].diff_against(instance)
        changes: list[ModelChange] = delta.changes
        
        return {
            change.field: change.new
            for change in changes
        }
