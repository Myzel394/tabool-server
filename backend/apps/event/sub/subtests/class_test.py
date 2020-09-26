from datetime import date, timedelta

from django.core.exceptions import ValidationError

from apps.event.mixins.tests.class_test import ClassTestTestMixin
from apps.event.models import ClassTest
from apps.lesson.mixins.tests.associated_user import AssociatedUserTestMixin
from apps.utils import ClientTestMixin
from apps.utils.date import find_next_date_by_weekday

__all__ = [
    "ModelTest"
]


class ModelTest(ClassTestTestMixin, ClientTestMixin):
    def test_invalid_date(self):
        def func():
            self.Create_class_test(
                targeted_date=find_next_date_by_weekday(date.today(), 5)
            )
        
        self.Create_class_test()
        self.assertRaises(ValidationError, func)
    
    def test_create(self):
        with self.Login_user_as_context() as user:
            course = self.Create_course()
            
            response = self.client.post("/api/class-test/", {
                "information": "Bebi",
                "targeted_date": date.today() + timedelta(days=5),
                "course": course.id,
            }, content_type="application/json")
        
        self.assertStatusOk(response.status_code)


class QuerySetTest(ClassTestTestMixin, AssociatedUserTestMixin):
    def test_association(self):
        self.check_queryset_from_user(ClassTest)
