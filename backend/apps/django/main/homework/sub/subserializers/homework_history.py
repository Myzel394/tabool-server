from apps.django.utils.serializers import ModelHistoryDetailSerializerMixin, ModelHistoryListSerializerMixin
from ...models import Homework

__all__ = [
    "HomeworkHistoryDetailSerializer", "HomeworkHistoryListSerializer"
]


class HomeworkHistoryDetailSerializer(ModelHistoryDetailSerializerMixin):
    class Meta:
        model = Homework
        fields = ModelHistoryDetailSerializerMixin.Meta.fields


class HomeworkHistoryListSerializer(ModelHistoryListSerializerMixin):
    class Meta:
        model = Homework
        fields = ModelHistoryListSerializerMixin.Meta.fields
