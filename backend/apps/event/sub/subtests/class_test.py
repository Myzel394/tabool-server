from datetime import date

from django.core.exceptions import ValidationError

from apps.event.mixins.tests.class_test import ClassTestTestMixin
from apps.event.models import ClassTest
from apps.lesson.mixins.tests.associated_user import AssociatedUserTestMixin
from apps.utils.date import find_next_date_by_weekday

__all__ = [
    "ModelTest"
]


class ModelTest(ClassTestTestMixin):
    def test_invalid_date(self):
        def func():
            self.Create_class_test(
                targeted_date=find_next_date_by_weekday(date.today(), 5)
            )
        
        self.Create_class_test()
        self.assertRaises(ValidationError, func)


class QuerySetTest(ClassTestTestMixin, AssociatedUserTestMixin):
    def test_association(self):
        self.check_queryset_from_user(ClassTest)
