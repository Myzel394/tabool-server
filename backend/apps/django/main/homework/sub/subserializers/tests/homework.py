from apps.django.utils.serializers import serializer_no_readonly_fields_factory
from ....serializers import DetailHomeworkSerializer

__all__ = [
    "HomeworkDetailSerializerTest"
]

HomeworkDetailSerializerTest = serializer_no_readonly_fields_factory(DetailHomeworkSerializer)
