from apps.django.utils.serializers import WritableFromUserFieldMixin
from ...models import Submission

__all__ = [
    "SubmissionField"
]


class SubmissionField(WritableFromUserFieldMixin):
    model = Submission
