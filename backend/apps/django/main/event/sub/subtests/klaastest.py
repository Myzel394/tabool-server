from datetime import timedelta

from django.core.exceptions import ValidationError

from apps.django.main.event.mixins.tests import *
from apps.django.main.event.sub.subserializers import *
from apps.django.main.lesson.mixins.tests import *
from apps.django.utils.tests import *
from apps.utils.dates import find_next_date_by_weekday


class ModelTest(ClasstestTestMixin, ClientTestMixin):
    def test_invalid_date(self):
        def func():
            self.Create_classtest(
                targeted_date=find_next_date_by_weekday(date.today(), 5)
            )
        
        self.Create_classtest()
        self.assertRaises(ValidationError, func)
    
    def test_create(self):
        with self.Login_user_as_context() as user:
            course = self.Create_course()
            
            response = self.client.post(f"/api/data/classtest/", {
                "information": "Bebi",
                "targeted_date": find_next_date_by_weekday(date.today() + timedelta(days=5), 1),
                "course": course.id,
            }, content_type="application/json")
        
        self.assertStatusOk(response.status_code)
    
    def test_filtering(self):
        with self.Login_user_as_context() as user:
            self.__class__.associated_user = user
            
            for _ in range(50):
                self.Create_classtest()
            
            targeted_date = date.today() + timedelta(days=2)
            filter_statement = "targeted_date"
            
            print("Classtests for user:", Classtest.objects.from_user(user).count())
            print("Classtests for user filtered:", Classtest.objects.from_user(user).filter(
                targeted_date__lte=targeted_date).count())
            
            response = self.client.get(
                f"/api/data/classtest/",
                {
                    filter_statement: targeted_date
                },
                content_type="application/json"
            )
            
            self.assertStatusOk(response.status_code)
            
            expected = Classtest.objects.from_user(user).filter(**{filter_statement: targeted_date})
            expected = ClasstestListSerializer(expected, many=True).data
            
            self.assertCountEqual(expected, response.data["results"])


class QuerySetTest(ClasstestTestMixin, AssociatedUserTestMixin):
    def test_association(self):
        self.check_queryset_from_user(Classtest)
