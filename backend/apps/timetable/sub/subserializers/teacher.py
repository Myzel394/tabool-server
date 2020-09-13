from apps.timetable.models import Teacher
from apps.utils.serializers import IdMixinSerializer

__all__ = [
    "TeacherSerializer"
]


class TeacherSerializer(IdMixinSerializer):
    class Meta:
        model = Teacher
        fields = ["first_name", "last_name", "email", "id"]
