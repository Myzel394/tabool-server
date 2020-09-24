from apps.utils.serializers import RandomIDSerializerMixin
from ...models import Subject

__all__ = [
    "SubjectDetailSerializer"
]


class SubjectDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Subject
        fields = ["name", "color", "id"]
