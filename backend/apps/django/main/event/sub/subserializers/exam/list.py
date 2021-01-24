from typing import *

from django_common_utils.libraries.utils import create_short
from rest_framework import serializers

from apps.django.main.lesson.public.serializer_fields.course import CourseField
from .base import BaseExamSerializer

if TYPE_CHECKING:
    from ....models import Exam

__all__ = [
    "ListExamSerializer"
]


class ListExamSerializer(BaseExamSerializer):
    class Meta(BaseExamSerializer.Meta):
        fields = [
            "course", "targeted_date", "truncated_information", "id"
        ]
    
    course = CourseField()
    
    truncated_information = serializers.SerializerMethodField()
    
    @staticmethod
    def get_truncated_information(instance: "Exam") -> Optional[str]:
        if instance.information:
            return create_short(instance.information)
        return
