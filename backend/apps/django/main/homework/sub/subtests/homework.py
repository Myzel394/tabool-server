from django.test import RequestFactory

from apps.django.main.homework.mixins.tests import HomeworkTestMixin
from apps.django.main.homework.models import Homework
from apps.django.main.homework.serializers import *
from apps.django.main.lesson.mixins.tests import *
from apps.django.utils.tests import ClientTestMixin


class HomeworkTest(HomeworkTestMixin, ClientTestMixin):
    def setUp(self) -> None:
        self.first_user = self.Login_user()
        
        self.course = self.Create_course()
        self.course.participants.add(self.first_user)
        self.lesson = self.Create_lesson(
            course=self.course
        )
        
        self.private_homework = self.Create_homework(
            lesson=self.lesson,
            private_to_user=self.first_user
        )
    
    def create_public_homework(self):
        return self.Create_homework(
            lesson=self.lesson
        )
    
    def test_public_cant_change_private_homework(self):
        # Login as another user
        with self.Login_user_as_context() as public_user:
            # Add to course, otherwise it would block the request because the user isn't a participant
            self.course.participants.add(public_user)
            
            # Try GET
            response = self.client.get(f"/api/data/homework/{self.private_homework.id}/")
            self.assertStatusNotOk(response.status_code)
            self.assertEqual(404, response.status_code)  # 404 is more secure than 403
            
            # Try PATCH
            response = self.client.patch(f"/api/data/homework/{self.private_homework.id}/", {
                "information": "test"
            })
            self.assertStatusNotOk(response.status_code)
            self.assertEqual(404, response.status_code)  # 404 is more secure than 403
    
    def test_private_user_can_change_private_homework(self):
        response = self.client.patch(f"/api/data/homework/{self.private_homework.id}/", {
            "information": "test"
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
    
    def test_users_cant_update_public_homework(self):
        public_homework = self.create_public_homework()
        
        response = self.client.patch(f"/api/data/homework/{public_homework.id}/", {
            "information": "test"
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)
        self.assertEqual(403, response.status_code)


class SerializerTest(HomeworkTestMixin, ClientTestMixin):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
        self.__class__.associated_user = self.logged_user
        self.homework = self.Create_homework(private_to_user=self.logged_user)
    
    def get_request(self):
        request = RequestFactory()
        request = request.put(f"/api/data/homework/{self.homework.id}/", {
            "information": "Test"
        }, content_type="application/json")
        request.user = self.logged_user
        return request
    
    def test_return_uses_detail_serializer(self):
        # Just edit something
        response = self.client.put(f"/api/data/homework/{self.homework.id}/", {
            "information": "Test"
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
        
        expected = DetailHomeworkSerializer(instance=self.homework, context={
            "request": self.get_request()
        }).data
        
        self.assertCountEqual(expected, response.data)


class QuerySetTest(HomeworkTestMixin, AssociatedUserTestMixin):
    def test_association(self):
        self.check_queryset_from_user(Homework)
