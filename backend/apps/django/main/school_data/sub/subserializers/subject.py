from apps.django.utils.serializers import RandomIDSerializerMixin, UserRelationField
from .user_relations import UserSubjectRelationSerializer
from ... import constants
from ...models import Subject

__all__ = [
    "SubjectSerializer"
]


class SubjectSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Subject
        fields = [
            "name", "short_name", "id", "user_relation"
        ]
        read_only = [
            "id", "user_relation"
        ]
    
    user_relation = UserRelationField(
        UserSubjectRelationSerializer,
        default=lambda subject, _: {
            "color": constants.SUBJECT_COLORS_MAPPING.get(
                subject.short_name, "#232323"
            )
        }
    )
