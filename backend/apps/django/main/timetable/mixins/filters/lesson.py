from django_filters import rest_framework as filters

__all__ = [
    "LessonFilterSetMixin"
]


class LessonFilterSetMixin(filters.FilterSet):
    lesson = filters.CharFilter(
        field_name="lesson__id",
    )
    
    lesson_date = filters.DateFilter(
        field_name="lesson__date",
    )
