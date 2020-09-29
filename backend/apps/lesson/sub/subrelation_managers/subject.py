from apps.relation_managers.managers import SimpleAllUserRelationManagerMixin
from ...models import Subject

__all__ = [
    "SubjectRelationManager"
]


class SubjectRelationManager(SimpleAllUserRelationManagerMixin):
    class Meta:
        model = Subject
