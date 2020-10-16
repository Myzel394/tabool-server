from rest_framework import serializers

from apps.django.main.school_data.public.serializer_fields import SubjectField, TeacherField
from apps.django.utils.serializers import RandomIDSerializerMixin
from ...models import Course


class CourseListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Course
        fields = [
            "subject", "id"
        ]
    
    subject = SubjectField()


class CourseDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Course
        fields = [
            "subject", "teacher", "course_number", "participants_count", "id"
        ]
    
    subject = SubjectField()
    teacher = TeacherField()
    
    participants_count = serializers.SerializerMethodField()
    
    @staticmethod
    def get_participants_count(obj: Course):
        return obj.participants.all().count()
