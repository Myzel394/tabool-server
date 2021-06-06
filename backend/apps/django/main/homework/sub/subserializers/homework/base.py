from typing import *

from django_common_utils.libraries.utils import create_short
from rest_framework import serializers

from apps.django.utils.serializers import ValidationSerializer
from ....models import Homework

__all__ = [
    "BaseHomeworkSerializer", "TruncatedInformationSerializerMixin"
]


class BaseHomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework


class TruncatedInformationSerializerMixin(ValidationSerializer):
    truncated_information = serializers.SerializerMethodField()
    
    @staticmethod
    def get_truncated_information(instance: Homework) -> Optional[str]:
        if instance.information:
            return create_short(instance.information)
        return
