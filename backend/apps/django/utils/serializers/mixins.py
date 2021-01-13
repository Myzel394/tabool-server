from abc import abstractmethod
from typing import *

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from simple_history.models import ModelChange, ModelDelta

from apps.django.utils import constants as utils_constants
from apps.django.utils.serializers import HistoryUserField
from apps.utils.files import privatize_file
from apps.utils.texts import camel_to_snake

__all__ = [
    "RandomIDSerializerMixin", "AssociatedUserSerializerMixin", "ScoosoScraperSerializerMixin",
    "PrivatizeSerializerMixin", "GetOrCreateSerializerMixin", "ModelHistoryListSerializerMixin",
    "ModelHistoryDetailSerializerMixin", "PreferredIdsMixin"
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


class ScoosoScraperSerializerMixin(serializers.Serializer):
    class Meta:
        model: M
        scooso_model: S
        model_scooso_relation_field_name: Optional[str] = None
    
    scooso_id = serializers.IntegerField(min_value=0)
    
    def pop_scooso_data(self, validated_data: dict) -> dict:
        return {
            "scooso_id": validated_data.pop("scooso_id"),
        }
    
    def get_unique_data(self, validated_data: dict) -> dict:
        return validated_data
    
    def get_extra_data(self, validated_data: dict) -> dict:
        return {}
    
    def rename_data(self, validated_data: dict) -> dict:
        return validated_data
    
    def get_scooso_relation_field_name(self) -> str:
        return getattr(self.Meta, "model_scooso_relation_field_name", None) or camel_to_snake(self.Meta.model.__name__)
    
    def create(self, validated_data) -> M:
        scooso_instance: S
        model_instance: M
        
        # Preparation - Get data
        scooso_data = self.pop_scooso_data(validated_data)
        renamed_data = self.rename_data(validated_data)
        field_name = self.get_scooso_relation_field_name()
        unique_data = self.get_unique_data(renamed_data)
        extra_data = self.get_extra_data(validated_data)
        unique_data.update(extra_data)
        update_data = {
            key: value
            for key, value in renamed_data.items()
            if key not in unique_data
        }
        
        # Create instances
        model_instance, _ = self.Meta.model.objects.get_or_create(
            **unique_data
        )
        scooso_instance, _ = self.Meta.scooso_model.objects.get_or_create(
            **{
                field_name: model_instance,
            }
        )
        
        # Set values
        for key, value in scooso_data.items():
            setattr(scooso_instance, key, value)
        scooso_instance.save()
        
        for key, value in update_data.items():
            setattr(model_instance, key, value)
        model_instance.save()
        
        return model_instance


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


class PreferredIdsMixin(serializers.ModelSerializer):
    preferred_id_key: str
    
    def is_preferring_id(self):
        assert "request" in self.context, "`request` missing in `context`."
        
        request = self.context["request"]
        
        if value := request.META.get(utils_constants.PREFERRED_IDS_HEADER_NAME):
            return self.instance.id in value.get(self.preferred_id_key, [])
        return False
    
    @property
    def data(self) -> Union[OrderedDict, str]:
        if self.is_preferring_id():
            return self.instance.id
        return super().data
