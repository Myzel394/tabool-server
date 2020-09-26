from apps.utils.serializers import WritableAllFieldMixin, WritableFromUserFieldMixin
from ..models import Course, Lesson, LessonData, Room, Subject, Teacher

__all__ = [
    "CourseField", "LessonField", "LessonDataField", "RoomField", "SubjectField", "TeacherField"
]


class CourseField(WritableFromUserFieldMixin):
    model = Course


class LessonField(WritableFromUserFieldMixin):
    model = Lesson


class LessonDataField(WritableFromUserFieldMixin):
    model = LessonData


class RoomField(WritableAllFieldMixin):
    model = Room


class SubjectField(WritableAllFieldMixin):
    model = Subject


class TeacherField(WritableAllFieldMixin):
    model = Teacher
