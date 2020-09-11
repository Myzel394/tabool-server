from apps.utils.serializers import IdMixinSerializer

from ..models import Teacher

__all__ = [
    "TeacherSerializer"
]


class TeacherSerializer(IdMixinSerializer):
    class Meta:
        model = Teacher
        fields = ["first_name", "last_name", "email", "id"]
