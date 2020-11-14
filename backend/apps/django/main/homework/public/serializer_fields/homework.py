from apps.django.main.homework.models import Homework
from apps.django.main.homework.sub.subserializers.homework import HomeworkDetailSerializer
from apps.django.utils.serializers import WritableFromUserFieldMixin

__all__ = [
    "HomeworkField"
]


class HomeworkField(WritableFromUserFieldMixin):
    model = Homework
    detail_serializer = HomeworkDetailSerializer
