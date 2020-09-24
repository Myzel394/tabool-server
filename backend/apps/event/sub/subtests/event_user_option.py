from apps.lesson.mixins.tests.associated_user import AssociatedUserTestMixin
from ...models import EventUserOption

__all__ = [
    "QuerySetTest"
]


class QuerySetTest(AssociatedUserTestMixin):
    def test_association(self):
        self.check_queryset_from_user(EventUserOption)
