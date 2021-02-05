from apps.django.utils.serializers import WritableFromUserFieldMixin
from ...models import Homework

__all__ = [
    "HomeworkField"
]


class HomeworkField(WritableFromUserFieldMixin):
    model = Homework
