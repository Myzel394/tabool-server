from apps.django.utils.serializers import WritableFromUserFieldMixin
from ...models import Submission
from ...serializers import DetailSubmissionSerializer

__all__ = [
    "SubmissionField"
]


class SubmissionField(WritableFromUserFieldMixin):
    model = Submission
    detail_serializer = DetailSubmissionSerializer
