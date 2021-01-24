from apps.django.utils.serializers import WritableFromUserFieldMixin
from ...models import Exam
from ...sub.subserializers.exam.detail import DetailExamSerializer

__all__ = [
    "ExamField"
]


class ExamField(WritableFromUserFieldMixin):
    model = Exam
    detail_serializer = DetailExamSerializer
