from apps.subject.mixins.tests import LessonTestMixin
from apps.subject.mixins.tests.associated_user import AssociatedUserTestMixin
from apps.subject.models import Lesson

__all__ = [
    "QuerySetTest"
]


class QuerySetTest(LessonTestMixin, AssociatedUserTestMixin):
    def test_association(self):
        self.check_queryset_from_user(Lesson)
