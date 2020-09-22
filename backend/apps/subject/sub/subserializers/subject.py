from apps.utils.serializers import IdMixinSerializer
from ...models import Subject

__all__ = [
    "SubjectDetailSerializer"
]


class SubjectDetailSerializer(IdMixinSerializer):
    class Meta:
        model = Subject
        fields = ["name", "color", "id"]
