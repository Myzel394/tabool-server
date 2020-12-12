from datetime import datetime

from django_common_utils.libraries.utils import model_verbose
from django_filters import rest_framework as filters
from django_hint import QueryType

from apps.django.main.lesson.models import Course
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
    
    course = filters.CharFilter(
        field_name="lesson__lesson_data__course__id",
        label=model_verbose(Course)
    )
    
    lesson_date__lte = filters.DateTimeFilter(method="lesson_date_filter_lte")
    lesson_date__gte = filters.DateTimeFilter(method="lesson_date_filter_gte")
    
    def lesson_date_filter_lte(self, qs: QueryType[Material], value: datetime, *args, **kwargs):
        return qs.filter(
            lesson__date__exact=value.date(),
            lesson__lesson_data__start_time__lte=value.time()
        )
    
    def lesson_date_filter_gte(self, qs: QueryType[Material], value: datetime, *args, **kwargs):
        return qs.filter(
            lesson__date__exact=value.date(),
            lesson__lesson_data__start_time__gte=value.time()
        )
