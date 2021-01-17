from apps.django.utils.serializers import WritableFromUserFieldMixin
from ...models import Poll
from ...serializers import PollSerializer

__all__ = [
    "PollField"
]


class PollField(WritableFromUserFieldMixin):
    model = Poll
    detail_serializer = PollSerializer
