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
        }
    
    type = filters.CharFilter(
        field_name="type__iexact",
        label=field_verbose(Homework, "type")
    )
    
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

    ignore = filters.BooleanFilter(
        field_name="userhomeworkrelation__ignore",
        label=field_verbose(UserHomeworkRelation, "ignore")
    )
