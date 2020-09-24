import lorem

from apps.homework.mixins.tests.homework import HomeworkTestMixin
from apps.homework.models import Homework
from apps.homework.sub.subserializers import (HomeworkDetailSerializer, HomeworkListSerializer)
from apps.lesson.mixins.tests.associated_user import AssociatedUserTestMixin
from apps.utils.tests import ClientTestMixin

__all__ = [
    "APITest", "QuerySetTest"
]


class APITest(HomeworkTestMixin, ClientTestMixin):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
        self.__class__.associated_user = self.logged_user
    
    def test_receive(self):
        homework = self.Create_homework()
        
        response = self.client.get("/api/user-homework/")
        
        self.assertStatusOk(response.status_code)
        
        self.assertCountEqual(
            response.data,
            HomeworkListSerializer(
                Homework.objects.all().from_user(self.logged_user),
                many=True
            ).data
        )
    
    def test_create_user_homework(self):
        homework = self.Create_homework()
        homework.delete()
        
        response = self.client.post(
            "/api/user-homework/",
            HomeworkDetailSerializer(homework).data,
            content_type="application/json"
        )
        
        print(response.data)
        self.assertStatusOk(response.status_code)
        
        self.assertTrue(Homework.objects.all().exists())
    
    def test_update_user_homework(self):
        homework = self.Create_homework()
        new_information = lorem.sentence()
        
        print(Homework.objects.from_user(self.logged_user))
        
        response = self.client.patch(
            f"/api/user-homework/{homework.id}/",
            {
                "information": new_information
            },
            content_type="application/json"
        )
        
        print(response.data)
        self.assertStatusOk(response.status_code)
        
        homework.refresh_from_db(fields=["information"])
        self.assertEqual(homework.information, new_information)
    
    def test_filtering(self):
        # This homework should not be found
        
        lesson = self.Create_lesson()
        self.Create_homework(
            lesson=lesson
        )
        
        response = self.client.get("/api/user-homework/", {
            "lesson": lesson.id
        }, content_type="application/json")
        
        self.assertStatusOk(response.status_code)
        
        expected_homeworks = Homework \
            .objects \
            .all() \
            .from_user(self.logged_user) \
            .filter(lesson__id=lesson.id)
        expected_data = HomeworkListSerializer(expected_homeworks, many=True).data
        actual_data = response.data
        
        self.assertCountEqual(actual_data, expected_data)


class QuerySetTest(HomeworkTestMixin, AssociatedUserTestMixin):
    def test_association(self):
        self.check_queryset_from_user(Homework)
