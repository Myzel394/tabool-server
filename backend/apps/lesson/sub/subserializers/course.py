from drf_writable_nested.serializers import WritableNestedModelSerializer

from apps.utils.serializers import RandomIDSerializerMixin, AssociatedUserSerializerMixin
from .subject import SubjectDetailSerializer
from .teacher import TeacherDetailSerializer
from ...models import Course


class CourseListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Course
        fields = [
            "subject", "name", "id"
        ]

    subject = SubjectDetailSerializer()


class CourseDetailSerializer(RandomIDSerializerMixin, AssociatedUserSerializerMixin, WritableNestedModelSerializer):
    class Meta:
        model = Course
        fields = [
            "subject", "teacher", "name", "id"
        ]
    
    subject = SubjectDetailSerializer()
    teacher = TeacherDetailSerializer()


