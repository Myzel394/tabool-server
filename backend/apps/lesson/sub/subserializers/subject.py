from apps.utils.serializers import RandomIDSerializerMixin
from .user_relations import UserSubjectRelationSerializer
from ...models import Subject

__all__ = [
    "SubjectDetailSerializer"
]


class SubjectDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Subject
        fields = [
            "name", "short_name", "color", "id", "user_relation"
        ]
        read_only_fields = [
            "id", "user_relation"
        ]
    
    user_relation = UserSubjectRelationSerializer(read_only=True)
