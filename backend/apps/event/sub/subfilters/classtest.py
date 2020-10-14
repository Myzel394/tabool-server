from django_common_utils.libraries.utils import model_verbose
from django_filters import rest_framework as filters

from apps.lesson.models import Course
from apps.school_data.models import Subject
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
    
    course = filters.CharFilter(
        field_name="course__id",
        label=model_verbose(Course)
    )
    
    subject = filters.CharFilter(
        field_name="course__subject__id",
        label=model_verbose(Subject)
    )
