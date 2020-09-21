from apps.utils.serializers import IdMixinSerializer
from ...models import Subject

__all__ = [
    "SubjectSerializer"
]


class SubjectSerializer(IdMixinSerializer):
    class Meta:
        model = Subject
        fields = ["name", "color", "id"]
