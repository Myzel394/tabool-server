from django_filters import rest_framework as filters

from apps.django.main.course.public import model_names as course_names
from apps.django.main.timetable.mixins import LessonFilterSetMixin
from ...models import Classbook

__all__ = [
    "ClassbookFilterSet"
]


class ClassbookFilterSet(LessonFilterSetMixin):
    class Meta:
        model = Classbook
        fields = {
            "presence_content": ["trigram_similar"],
            "online_content": ["trigram_similar"],
            "video_conference_link": ["exact", "isnull"]
        }

    course = filters.CharFilter(
        field_name="lesson__course__id",
        label=course_names.COURSE
    )
