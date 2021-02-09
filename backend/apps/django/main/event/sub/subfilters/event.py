from django_filters import filterset, rest_framework as filters

from apps.django.main.course.public import model_names as course_names
from ...models import Event

__all__ = [
    "EventFilterSet"
]


class EventFilterSet(filterset.FilterSet):
    class Meta:
        model = Event
        fields = {
            "start_datetime": ["lte", "gte"],
            "end_datetime": ["exact"],
        }
    
    room = filters.CharFilter(
        field_name="room__id",
        label=course_names.ROOM,
    )
