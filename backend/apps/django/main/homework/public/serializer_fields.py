from apps.utils.serializers import WritableFromUserFieldMixin
from ..models import Homework, Submission

__all__ = [
    "HomeworkField", "SubmissionField"
]


class HomeworkField(WritableFromUserFieldMixin):
    model = Homework


class SubmissionField(WritableFromUserFieldMixin):
    model = Submission
