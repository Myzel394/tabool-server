from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from .base import BaseLessonAbsenceSerializer

__all__ = [
    "DetailLessonAbsenceSerializer"
]


class DetailLessonAbsenceSerializer(BaseLessonAbsenceSerializer):
    class Meta(BaseLessonAbsenceSerializer.Meta):
        fields = ["lesson", "reason", "is_signed", "id"]
    
    lesson = LessonField()
