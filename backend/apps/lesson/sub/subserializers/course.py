from rest_framework import serializers

from apps.utils.serializers import RandomIDSerializerMixin
from ...models import Course
from ...public.serializer_fields import SubjectField, TeacherField


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
