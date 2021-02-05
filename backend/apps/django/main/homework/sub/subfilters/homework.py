from django_common_utils.libraries.utils import field_verbose
from django_filters import rest_framework as filters

from apps.django.main.course.public import model_names as course_names
from apps.django.main.timetable.mixins import LessonFilterSetMixin
from ...models import Homework

__all__ = [
    "HomeworkFilterSet"
]


class HomeworkFilterSet(LessonFilterSetMixin):
    class Meta:
        model = Homework
        fields = {
            "due_date": ["lte", "gte"],
            "type": ["exact"],
        }
    
    type = filters.CharFilter(
        field_name="type__iexact",
        label=field_verbose(Homework, "type")
    )
    
    course = filters.CharFilter(
        field_name="lesson__course__id",
        label=course_names.COURSE
    )
