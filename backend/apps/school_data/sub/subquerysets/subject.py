from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

from apps.school_data.models.user_relations.subject import UserSubjectRelation
from apps.utils.querysets import RelationAllUserQuerySetMixin

__all__ = [
    "SubjectQuerySet"
]


class SubjectQuerySet(CustomQuerySetMixin.QuerySet, RelationAllUserQuerySetMixin):
    related_model = UserSubjectRelation
