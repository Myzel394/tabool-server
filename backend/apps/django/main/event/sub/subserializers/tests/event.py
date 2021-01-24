from apps.django.main.event.sub.subserializers.event.detail import DetailEventSerializer
from apps.django.utils.serializers import serializer_no_readonly_fields_factory

__all__ = [
    "EventDetailSerializerTest"
]

EventDetailSerializerTest = serializer_no_readonly_fields_factory(DetailEventSerializer)
