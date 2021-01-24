from apps.django.main.lesson.mixins.tests import *
from apps.django.main.lesson.mixins.tests.associated_user import *
from apps.django.main.lesson.models import *

__all__ = [
    "QuerySetTest"
]


class QuerySetTest(LessonTestMixin, AssociatedUserTestMixin):
    def test_association(self):
        self.check_queryset_from_user(Lesson)
        self.check_queryset_from_user(Course)
