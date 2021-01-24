from apps.django.utils.serializers import WritableAllFieldMixin
from ...models import Subject
from ...sub.subserializers.subject import SubjectSerializer

__all__ = [
    "SubjectField"
]


class SubjectField(WritableAllFieldMixin):
    model = Subject
    detail_serializer = SubjectSerializer
