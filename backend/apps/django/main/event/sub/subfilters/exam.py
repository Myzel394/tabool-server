from django_common_utils.libraries.utils import model_verbose
from django_filters import rest_framework as filters

from apps.django.main.lesson.models import Course
from apps.django.main.school_data.models import Subject
from ...models import Exam

__all__ = [
    "ExamFilterSet"
]


class ExamFilterSet(filters.FilterSet):
    class Meta:
        model = Exam
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
