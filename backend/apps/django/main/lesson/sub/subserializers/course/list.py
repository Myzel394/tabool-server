from apps.django.main.school_data.public.serializer_fields.subject import SubjectField
from apps.django.main.school_data.public.serializer_fields.teacher import TeacherField
from .base import BaseCourseSerializer

__all__ = [
    "ListCourseSerializer"
]


class ListCourseSerializer(BaseCourseSerializer):
    class Meta(BaseCourseSerializer.Meta):
        fields = [
            "subject", "teacher", "course_number", "id"
        ]
    
    subject = SubjectField(detail=True)
    teacher = TeacherField(detail=True)
