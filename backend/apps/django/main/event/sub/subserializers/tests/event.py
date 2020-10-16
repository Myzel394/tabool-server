from apps.django.main.event.sub.subserializers import EventDetailSerializer
from apps.django.utils.serializers import serializer_no_readonly_fields_factory

__all__ = [
    "EventDetailSerializerTest"
]

EventDetailSerializerTest = serializer_no_readonly_fields_factory(EventDetailSerializer)
