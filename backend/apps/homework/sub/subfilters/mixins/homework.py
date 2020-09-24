from django_common_utils.libraries.utils import model_verbose
from django_filters import rest_framework as filters

from apps.subject.models import Lesson, Subject

__all__ = [
    "BaseHomeworkFilterSetMixin"
]


class BaseHomeworkFilterSetMixin(filters.FilterSet):
    lesson = filters.CharFilter(
        field_name="lesson__id",
        label=model_verbose(Lesson)
    )
    
    subject = filters.CharFilter(
        field_name="lesson__lesson_data__subject__id",
        label=model_verbose(Subject)
    )
