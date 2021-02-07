from rest_framework import serializers
from simple_history.models import ModelChange, ModelDelta

from apps.django.utils.serializers import HistoryUserField

__all__ = [
    "GetOrCreateSerializerMixin", "ModelHistoryListSerializerMixin",
    "ModelHistoryDetailSerializerMixin"
]


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
