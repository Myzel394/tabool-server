from django_common_utils.libraries.utils import model_verbose
from django_filters import rest_framework as filters

from apps.subject.models import Subject
from ...models import UserHomework

__all__ = [
    "UserHomeworkFilterSet"
]


class UserHomeworkFilterSet(filters.FilterSet):
    class Meta:
        model = UserHomework
        fields = ["lesson", ]
    
    lesson = filters.CharFilter(
        field_name="lesson__id",
        label=model_verbose(UserHomework)
    )
    
    subject = filters.CharFilter(
        field_name="lesson__lesson_data__subject__id",
        label=model_verbose(Subject)
    )
    
    due_date__lte = filters.DateFilter(
        field_name="due_date",
        lookup_expr="lte"
    )
    
    due_date__gte = filters.DateFilter(
        field_name="due_date",
        lookup_expr="gte"
    )
    
    completed = filters.BooleanFilter(
        field_name="completed",
    )
