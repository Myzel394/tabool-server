from apps.django.main.timetable.public.serializer_fields.lesson import LessonField
from .base import BaseSubmissionSerializer

__all__ = [
    "CreateSubmissionSerializer"
]


class CreateSubmissionSerializer(BaseSubmissionSerializer):
    class Meta(BaseSubmissionSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "publish_datetime", "file", "name"
        ]
    
    lesson = LessonField()
    
    # TODO: Add tests!
    def create(self, validated_data):
        validated_data["student"] = self.context["request"].user.student
        
        return super().create(validated_data)
