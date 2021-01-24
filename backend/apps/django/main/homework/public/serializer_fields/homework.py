from apps.django.utils.serializers import WritableFromUserFieldMixin
from ...models import Homework
from ...sub.subserializers.homework.detail import DetailHomeworkSerializer

__all__ = [
    "HomeworkField"
]


class HomeworkField(WritableFromUserFieldMixin):
    model = Homework
    detail_serializer = DetailHomeworkSerializer
