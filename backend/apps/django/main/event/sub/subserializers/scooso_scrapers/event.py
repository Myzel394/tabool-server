from django_common_utils.libraries.handlers.mixins import BaseHandlerMixin
from django_common_utils.libraries.utils import ensure_iteration

from apps.django.utils.serializers import GetOrCreateSerializerMixin
from ....models import Event

__all__ = [
    "EventScoosoScraperSerializer"
]


class EventScoosoScraperSerializer(GetOrCreateSerializerMixin):
    class Meta:
        model = Event
        fields = [
            "title", "start_datetime", "end_datetime"
        ]
    
    def create(self, validated_data):
        handlers = Event.handlers()["title"]
        title = validated_data.pop("title")
        for handler in ensure_iteration(handlers, lambda element: issubclass(element.__class__, BaseHandlerMixin)):
            title = handler.handle(title)
        
        return Event.objects.get_or_create(
            title__iexact=title,
            defaults={
                "title": title,
                **validated_data
            },
        )[0]
