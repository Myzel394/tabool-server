from apps.utils.serializers import RandomIDSerializerMixin
from ...models import Subject

__all__ = [
    "SubjectDetailSerializer"
]

# TODO: Automatically add extra fields to get the user relation data!


class SubjectDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Subject
        fields = ["name", "color", "id"]
