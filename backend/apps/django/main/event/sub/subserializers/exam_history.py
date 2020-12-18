from apps.django.utils.serializers import ModelHistoryDetailSerializerMixin, ModelHistoryListSerializerMixin
from ...models import Exam

__all__ = [
    "ExamHistoryDetailSerializer", "ExamHistoryListSerializer"
]


class ExamHistoryDetailSerializer(ModelHistoryDetailSerializerMixin):
    class Meta:
        model = Exam
        fields = ModelHistoryDetailSerializerMixin.Meta.fields


class ExamHistoryListSerializer(ModelHistoryListSerializerMixin):
    class Meta:
        model = Exam
        fields = ModelHistoryListSerializerMixin.Meta.fields
