from rest_framework import serializers

from ....models import Submission

__all__ = [
    "BaseSubmissionSerializer"
]


class BaseSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
