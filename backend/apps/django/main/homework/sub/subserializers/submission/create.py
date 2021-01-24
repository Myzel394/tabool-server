from typing import *

from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from apps.django.utils.serializers import PrivatizeSerializerMixin
from .base import BaseSubmissionSerializer

if TYPE_CHECKING:
    from ....models import Submission

__all__ = [
    "CreateSubmissionSerializer"
]


class CreateSubmissionSerializer(BaseSubmissionSerializer, PrivatizeSerializerMixin):
    class Meta(BaseSubmissionSerializer.Meta):
        fields = [
            "file", "privatize", "upload_date", "lesson"
        ]
    
    lesson = LessonField()
    
    def get_file_to_privatize(self, instance: "Submission", validated_data):
        return [instance.file.path]
    
    def create(self, validated_data):
        validated_data["associated_user"] = self.context["request"].user
        return super().create(validated_data)
