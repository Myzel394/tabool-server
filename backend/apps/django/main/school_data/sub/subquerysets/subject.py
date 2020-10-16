from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

from apps.django.main.school_data.models.user_relations.subject import UserSubjectRelation
from apps.django.utils.querysets import RelationAllUserQuerySetMixin

__all__ = [
    "SubjectQuerySet"
]


class SubjectQuerySet(CustomQuerySetMixin.QuerySet, RelationAllUserQuerySetMixin):
    related_model = UserSubjectRelation
