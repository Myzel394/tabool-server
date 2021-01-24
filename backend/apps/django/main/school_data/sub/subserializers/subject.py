from apps.django.extra.scooso_scraper.utils import rename_name_for_color_mapping
from apps.django.utils.serializers import PreferredIdsMixin, RandomIDSerializerMixin, UserRelationField
from .user_relations import UserSubjectRelationSerializer
from ... import constants
from ...models import Subject

__all__ = [
    "SubjectSerializer"
]


class SubjectSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "subject"
    
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
                rename_name_for_color_mapping(subject.name), "#232323"
            )
        }
    )
