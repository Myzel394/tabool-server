from apps.utils.serializers import RandomIDSerializerMixin
from ...models import Course
from ...public.serializer_fields import SubjectField, TeacherField


class CourseListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Course
        fields = [
            "subject", "name", "id"
        ]
    
    subject = SubjectField()


class CourseDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Course
        fields = [
            "subject", "teacher", "name", "id"
        ]
    
    subject = SubjectField()
    teacher = TeacherField()
