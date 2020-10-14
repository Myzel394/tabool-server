from apps.utils.serializers import WritableFromUserFieldMixin
from ..models import Course, Lesson, LessonData

__all__ = [
    "CourseField", "LessonField", "LessonDataField"
]


class CourseField(WritableFromUserFieldMixin):
    model = Course


class LessonField(WritableFromUserFieldMixin):
    model = Lesson


class LessonDataField(WritableFromUserFieldMixin):
    model = LessonData
