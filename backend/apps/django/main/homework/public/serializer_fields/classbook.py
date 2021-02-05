from apps.django.utils.serializers import WritableFromUserFieldMixin
from ...models import Classbook

__all__ = [
    "ClassbookField"
]


class ClassbookField(WritableFromUserFieldMixin):
    model = Classbook
