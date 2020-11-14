from apps.django.main.homework.models import Submission
from apps.django.main.homework.sub.subserializers.submission import SubmissionDetailSerializer
from apps.django.utils.serializers import WritableFromUserFieldMixin

__all__ = [
    "SubmissionField"
]


class SubmissionField(WritableFromUserFieldMixin):
    model = Submission
    detail_serializer = SubmissionDetailSerializer
