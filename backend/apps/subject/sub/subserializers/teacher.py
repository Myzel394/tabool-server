from apps.utils.serializers import IdMixinSerializer
from ...models import Teacher

__all__ = [
    "TeacherDetailSerializer"
]


class TeacherListSerializer(IdMixinSerializer):
    class Meta:
        model = Teacher
        fields = ["last_name", "short_name", "id"]


class TeacherDetailSerializer(IdMixinSerializer):
    class Meta:
        model = Teacher
        fields = ["first_name", "last_name", "short_name", "email", "id"]
