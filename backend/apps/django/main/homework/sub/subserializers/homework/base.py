from typing import *

from django_common_utils.libraries.utils import create_short
from rest_framework import serializers

from ....models import Homework

__all__ = [
    "BaseHomeworkSerializer", "TruncatedInformationSerializer", "IsPrivateMixin"
]


class BaseHomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework


class TruncatedInformationSerializer(serializers.Serializer):
    truncated_information = serializers.SerializerMethodField()
    
    def get_truncated_information(self, instance: Homework) -> Optional[str]:
        if instance.information:
            return create_short(instance.information)
        return


class IsPrivateMixin(serializers.Serializer):
    is_private = serializers.SerializerMethodField()
    
    @staticmethod
    def get_is_private(instance: Homework) -> bool:
        return instance.is_private
