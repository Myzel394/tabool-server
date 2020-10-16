from apps.django.utils.serializers import WritableAllFieldMixin
from ..models import Room, Subject, Teacher

__all__ = [
    "RoomField", "SubjectField", "TeacherField"
]


class RoomField(WritableAllFieldMixin):
    model = Room


class SubjectField(WritableAllFieldMixin):
    model = Subject


class TeacherField(WritableAllFieldMixin):
    model = Teacher
