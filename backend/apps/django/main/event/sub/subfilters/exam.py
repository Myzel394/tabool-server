from django_filters import rest_framework as filters

from apps.django.main.course.public import model_names as course_names
from apps.django.main.timetable.mixins import LessonFilterSetMixin
from ...models import Event

__all__ = [
    "ExamFilterSet"
]


class ExamFilterSet(LessonFilterSetMixin):
    class Meta:
        model = Event
        fields = {
            "date": ["lte", "gte"],
        }
    
    course = filters.CharFilter(
        field_name="course__id",
        label=course_names.COURSE,
    )
