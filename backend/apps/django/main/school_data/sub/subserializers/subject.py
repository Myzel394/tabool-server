from apps.django.utils.serializers import PreferredIdsMixin, RandomIDSerializerMixin, UserRelationField
from .user_relations import UserSubjectRelationSerializer
from ...models import Subject

__all__ = [
    "SubjectDetailSerializer"
]


class SubjectDetailSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "subject"
    
    class Meta:
        model = Subject
        fields = [
            "name", "short_name", "id", "user_relation"
        ]
        read_only_fields = [
            "id", "user_relation"
        ]
    
    user_relation = UserRelationField(UserSubjectRelationSerializer)
