from apps.django.utils.serializers import ModelHistoryDetailSerializerMixin, ModelHistoryListSerializerMixin
from ...models import Classtest

__all__ = [
    "ClasstestHistoryDetailSerializer", "ClasstestHistoryListSerializer"
]


class ClasstestHistoryDetailSerializer(ModelHistoryDetailSerializerMixin):
    class Meta:
        model = Classtest
        fields = ModelHistoryDetailSerializerMixin.Meta.fields


class ClasstestHistoryListSerializer(ModelHistoryListSerializerMixin):
    class Meta:
        model = Classtest
        fields = ModelHistoryListSerializerMixin.Meta.fields
