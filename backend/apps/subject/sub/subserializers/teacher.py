from apps.utils.serializers import RandomIDSerializerMixin
from ...models import Teacher

__all__ = [
    "TeacherDetailSerializer"
]


class TeacherListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Teacher
        fields = ["last_name", "short_name", "id"]
        read_only_fields = ["id"]


class TeacherDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Teacher
        fields = ["first_name", "last_name", "short_name", "email", "id"]
        read_only_fields = ["id"]
