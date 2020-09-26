from django_filters import rest_framework as filters

from ...models import Classtest

__all__ = [
    "ClasstestFilterSet"
]


class ClasstestFilterSet(filters.FilterSet):
    class Meta:
        model = Classtest
        fields = {
            "targeted_date": ["lte", "gte", "exact"],
        }
