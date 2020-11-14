from apps.django.main.event.sub.subserializers.event import EventDetailSerializer
from apps.django.utils.serializers import serializer_no_readonly_fields_factory

__all__ = [
    "EventDetailSerializerTest"
]

EventDetailSerializerTest = serializer_no_readonly_fields_factory(EventDetailSerializer)
