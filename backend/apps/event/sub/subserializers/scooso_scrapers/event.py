from rest_framework import serializers

from ....models import Event

__all__ = [
    "EventScoosoScraperSerializer"
]


class EventScoosoScraperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "title", "start_datetime", "end_datetime"
        ]
