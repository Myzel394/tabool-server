from django_filters import rest_framework as filters

from ...models import ClassTest

__all__ = [
    "ClassTestFilterSet"
]


class ClassTestFilterSet(filters.FilterSet):
    class Meta:
        model = ClassTest
        fields = {
            "targeted_date": ["lte", "gte", "exact"],
        }
