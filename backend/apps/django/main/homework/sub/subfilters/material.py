from django_filters import rest_framework as filters

from apps.django.main.course.public import model_names as course_names
from apps.django.main.timetable.mixins import LessonFilterSetMixin
from ...models import Material

__all__ = [
    "MaterialFilterSet"
]


class MaterialFilterSet(LessonFilterSetMixin):
    class Meta:
        model = Material
        fields = {
            "announce": ["exact"],
            "publish_datetime": ["lte", "gte"],
        }
    
    course = filters.CharFilter(
        field_name="lesson__course__id",
        label=course_names.COURSE
    )
