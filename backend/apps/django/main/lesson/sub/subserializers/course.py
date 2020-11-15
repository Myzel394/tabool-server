from rest_framework import serializers

from apps.django.main.school_data.public.serializer_fields.subject import SubjectField
from apps.django.main.school_data.public.serializer_fields.teacher import TeacherField
from apps.django.utils.serializers import PreferredIdsMixin, RandomIDSerializerMixin
from ...models import Course

__all__ = [
    "CourseDetailSerializer"
]


class CourseDetailSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "course"
    
    class Meta:
        model = Course
        fields = [
            "subject", "teacher", "course_number", "participants_count", "id"
        ]
    
    subject = SubjectField(detail=True)
    teacher = TeacherField(detail=True)
    
    participants_count = serializers.SerializerMethodField()
    
    @staticmethod
    def get_participants_count(obj: Course):
        return obj.participants.all().count()
