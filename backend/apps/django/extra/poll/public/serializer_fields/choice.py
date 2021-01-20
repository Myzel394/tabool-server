from apps.django.utils.serializers import WritableFromUserFieldMixin
from ...models import Choice
from ...sub.subserializers.choice import ChoiceSerializer

__all__ = [
    "ChoiceField"
]


class ChoiceField(WritableFromUserFieldMixin):
    model = Choice
    detail_serializer = ChoiceSerializer
