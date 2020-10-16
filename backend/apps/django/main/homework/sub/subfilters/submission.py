from django_common_utils.libraries.utils import model_verbose
from django_filters import rest_framework as filters

from apps.django.main.homework.models import Submission
from apps.django.main.lesson.models import Course, Lesson

__all__ = [
    "SubmissionFilterSet"
]


class SubmissionFilterSet(filters.FilterSet):
    class Meta:
        model = Submission
        fields = {
            "upload_at": ["lte", "gte"],
            "is_uploaded": ["exact"]
        }
    
    lesson = filters.CharFilter(
        field_name="lesson__id",
        label=model_verbose(Lesson)
    )
    
    course = filters.CharFilter(
        field_name="lesson__lesson_data__course__id",
        label=model_verbose(Course)
    )
