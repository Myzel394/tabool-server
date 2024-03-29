from rest_framework import serializers

from apps.django.utils.serializers import ValidationSerializer
from ....models import Submission

__all__ = [
    "BaseSubmissionSerializer", "SubmissionSizeSerializerMixin"
]


class BaseSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission


class SubmissionSizeSerializerMixin(ValidationSerializer):
    size = serializers.ReadOnlyField(source="file.size")
