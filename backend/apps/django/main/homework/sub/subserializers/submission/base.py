from rest_framework import serializers

from ....models import Submission

__all__ = [
    "BaseSubmissionSerializer", "SizeMixin"
]


class BaseSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission


class SizeMixin(serializers.Serializer):
    size = serializers.SerializerMethodField()
    
    def get_size(self, instance: Submission) -> int:
        return instance.file.size
