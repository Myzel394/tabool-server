from apps.django.main.event.models import Exam
from apps.django.main.event.sub.subserializers.exam import ExamDetailSerializer
from apps.django.utils.serializers import WritableFromUserFieldMixin

__all__ = [
    "ExamField"
]


class ExamField(WritableFromUserFieldMixin):
    model = Exam
    detail_serializer = ExamDetailSerializer
