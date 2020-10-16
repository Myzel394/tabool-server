from apps.django.utils.serializers import serializer_no_readonly_fields_factory
from ..homework import HomeworkDetailSerializer

__all__ = [
    "HomeworkDetailSerializerTest"
]

HomeworkDetailSerializerTest = serializer_no_readonly_fields_factory(HomeworkDetailSerializer)
