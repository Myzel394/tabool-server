from django_filters import rest_framework as filters

from apps.django.authentication.user.public import model_names as auth_names
from apps.django.main.course.public import model_names as course_names
from apps.django.main.timetable.mixins import LessonFilterSetMixin
from ...models import Event

__all__ = [
    "ModificationFilterSet"
]


class ModificationFilterSet(LessonFilterSetMixin):
    class Meta:
        model = Event
        fields = [
            "modification_type"
        ]
    
    new_room = filters.CharFilter(
        field_name="new_room__id",
        label=course_names.ROOM,
    )
    
    new_subject = filters.CharFilter(
        field_name="new_subject__id",
        label=course_names.SUBJECT,
    )
    
    new_teacher = filters.CharFilter(
        field_name="new_teacher__id",
        label=auth_names.TEACHER,
    )
