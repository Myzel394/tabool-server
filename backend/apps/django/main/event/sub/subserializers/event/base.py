from rest_framework import serializers

from ....models import Event

__all__ = [
    "BaseEventSerializer"
]


class BaseEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
