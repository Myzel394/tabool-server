from django_filters import rest_framework as filters

from apps.django.main.course.public import model_names as course_names
from apps.django.main.timetable.mixins import LessonFilterSetMixin
from ...models import Submission

__all__ = [
    "SubmissionFilterSet"
]


class SubmissionFilterSet(LessonFilterSetMixin):
    class Meta:
        model = Submission
        fields = {
            "publish_datetime": ["lte", "gte", "date__exact"]
        }
    
    course = filters.CharFilter(
        field_name="lesson__course__id",
        label=course_names.COURSE
    )
