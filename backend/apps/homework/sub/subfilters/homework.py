from django_common_utils.libraries.utils import model_verbose
from django_filters import rest_framework as filters

from apps.lesson.models import Lesson, Subject
from ...models import Homework

__all__ = [
    "HomeworkFilterSet"
]


class HomeworkFilterSet(filters.FilterSet):
    class Meta:
        model = Homework
        fields = {
            "due_date": ["lte", "gte"],
            "type": ["iexact"]
        }
    
    lesson = filters.CharFilter(
        field_name="lesson__id",
        label=model_verbose(Lesson)
    )
    
    subject = filters.CharFilter(
        field_name="lesson__lesson_data__subject__id",
        label=model_verbose(Subject)
    )
