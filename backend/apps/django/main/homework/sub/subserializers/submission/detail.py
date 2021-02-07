from apps.django.authentication.user.sub.subserializers.user import DetailUserSerializer
from apps.django.main.timetable.sub.subserializers.lesson import DetailLessonSerializer
from .base import BaseSubmissionSerializer

__all__ = [
    "StudentDetailSubmissionSerializer", "TeacherDetailSubmissionSerializer"
]


class StudentDetailSubmissionSerializer(BaseSubmissionSerializer):
    class Meta(BaseSubmissionSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "publish_datetime", "file", "name", "created_at" "id"
        ]
    
    lesson = DetailLessonSerializer()


class TeacherDetailSubmissionSerializer(BaseSubmissionSerializer):
    class Meta(BaseSubmissionSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "publish_datetime", "file", "name", "associated_user", "id"
        ]
    
    lesson = DetailLessonSerializer()
    associated_user = DetailUserSerializer()
