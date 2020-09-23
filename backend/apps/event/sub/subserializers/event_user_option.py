from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from .event import EventDetailSerializer, EventListSerializer
from ...models import EventUserOption


class EventUserOptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventUserOption
        fields = [
            "event", "id"
        ]
        read_only_fields = ["event", "id"]
    
    event = EventListSerializer()


class EventUserOptionDetailSerializer(WritableNestedModelSerializer):
    class Meta:
        model = EventUserOption
        fields = [
            "event", "ignore", "id"
        ]
        read_only_fields = ["event", "id"]
    
    event = EventDetailSerializer()
