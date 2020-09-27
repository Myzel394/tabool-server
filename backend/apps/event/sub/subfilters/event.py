from django_common_utils.libraries.utils import field_verbose, model_verbose
from django_filters import rest_framework as filters

from apps.lesson.models import Room
from ...models import Event, UserEventRelation

__all__ = [
    "EventFilterSet"
]


class EventFilterSet(filters.FilterSet):
    class Meta:
        model = Event
        fields = {
            "start_datetime": ["lte", "gte"],
            "end_datetime": ["lte", "gte"]
        }
    
    room = filters.CharFilter(
        field_name="room__id",
        label=model_verbose(Room)
    )
    
    ignore = filters.BooleanFilter(
        field_name="usereventrelation__ignore",
        label=field_verbose(UserEventRelation, "ignore")
    )
