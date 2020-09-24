from django_filters import rest_framework as filters
import django_filters

from apps.homework.models import UserHomework
from apps.subject.models import Lesson, Subject

__all__ = [
    "HomeworkFilterSet"
]


# TODO: Foreignkey filter on serializer
class HomeworkFilterSet(filters.FilterSet):
    class Meta:
        model = UserHomework
        fields = ["lesson", ]
    
    lesson = filters.ModelMultipleChoiceFilter(
        queryset=Lesson.objects.all(),
        field_name="lesson__id",
    )
