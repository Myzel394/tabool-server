from django.db.models import Q
from django_filters import rest_framework as filters
from django_hint import *

from ...models import LessonAbsence

__all__ = [
    "AbsenceFilterSet"
]


class AbsenceFilterSet(filters.FilterSet):
    class Meta:
        model = LessonAbsence
        fields = {
            "is_signed": ["exact"]
        }
    
    lesson__date__lte = filters.DateTimeFilter(field_name="lesson__date", lookup_expr="lte")
    lesson__date__gte = filters.DateTimeFilter(field_name="lesson__date", lookup_expr="gte")
    
    reason__is_null = filters.BooleanFilter(method="reason__isnull")
    
    def reason__isnull(self, qs: QueryType[LessonAbsence], name: str, value: bool, *args, **kwargs):
        if value:
            return qs \
                .only("reason") \
                .filter(Q(reason__isnull=True) | Q(reason__exact="")) \
                .distinct()
        return qs \
            .only("reason") \
            .filter(reason__isnull=False) \
            .exclude(reason="")
