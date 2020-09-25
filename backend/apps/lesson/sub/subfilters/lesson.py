from django_filters import rest_framework as filters

from ...models import Lesson

__all__ = [
    "LessonFilterSet"
]


class LessonFilterSet(filters.FilterSet):
    class Meta:
        model = Lesson
        fields = {
            "date": ["lte", "gte"],
        }
