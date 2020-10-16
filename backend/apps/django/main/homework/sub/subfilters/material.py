from django_common_utils.libraries.utils import model_verbose
from django_filters import rest_framework as filters

from apps.django.main.lesson.models import Course, Lesson
from ...models import Material

__all__ = [
    "MaterialFilterSet"
]


class MaterialFilterSet(filters.FilterSet):
    class Meta:
        model = Material
        fields = {
            "added_at": ["lte", "gte", "date__exact"]
        }
    
    lesson = filters.CharFilter(
        field_name="lesson__id",
        label=model_verbose(Lesson)
    )
    
    course = filters.CharFilter(
        field_name="lesson__lesson_data__course__id",
        label=model_verbose(Course)
    )
