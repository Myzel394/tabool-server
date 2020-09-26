from django_common_utils.libraries.utils import field_verbose, model_verbose
from django_filters import rest_framework as filters

from apps.lesson.models import Lesson, Subject
from ...models import Homework, UserHomeworkRelation

__all__ = [
    "HomeworkFilterSet"
]


class HomeworkFilterSet(filters.FilterSet):
    class Meta:
        model = Homework
        fields = {
            "due_date": ["lte", "gte", "exact"],
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
    
    completed = filters.BooleanFilter(
        field_name="userhomeworkrelation__completed",
        label=field_verbose(UserHomeworkRelation, "completed")
    )
