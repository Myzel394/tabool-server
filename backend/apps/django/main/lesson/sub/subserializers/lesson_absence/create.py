from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from .base import BaseLessonAbsenceSerializer

__all__ = [
    "CreateLessonAbsenceSerializer"
]


class CreateLessonAbsenceSerializer(BaseLessonAbsenceSerializer):
    class Meta(BaseLessonAbsenceSerializer.Meta):
        fields = BaseLessonAbsenceSerializer.Meta.fields + ["lesson"]
    
    lesson = LessonField()
    
    def create(self, validated_data):
        validated_data["associated_user"] = self.context["request"].user
        return super().create(validated_data)
