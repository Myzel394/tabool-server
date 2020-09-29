from django_common_utils.libraries.models import CustomQuerySetMixin

from apps.utils.querysets import RelationAllUserQuerySetMixin
from ...models.user_relations.subject import UserSubjectRelation


__all__ = [
    "SubjectQuerySet"
]


class SubjectQuerySet(CustomQuerySetMixin.QuerySet, RelationAllUserQuerySetMixin):
    related_model = UserSubjectRelation

