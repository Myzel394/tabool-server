from apps.school_data.models import Room, Subject, Teacher
from apps.utils.serializers import WritableAllFieldMixin


class RoomField(WritableAllFieldMixin):
    model = Room


class SubjectField(WritableAllFieldMixin):
    model = Subject


class TeacherField(WritableAllFieldMixin):
    model = Teacher
