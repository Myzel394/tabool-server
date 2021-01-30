import random
from pprint import pp

import lorem
from django.test import RequestFactory

from apps.django.main.homework.mixins.tests import HomeworkTestMixin
from apps.django.main.homework.models import Homework
from apps.django.main.homework.serializers import *
from apps.django.main.homework.sub.subserializers.tests import *
from apps.django.main.lesson.mixins.tests import *
from apps.django.utils.tests import ClientTestMixin


class APITest(HomeworkTestMixin, ClientTestMixin):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
        self.__class__.associated_user = self.logged_user
    
    def test_create_user_homework(self):
        homework = self.Create_homework()
        homework.delete()
        
        response = self.client.post(
            f"/api/data/homework/",
            HomeworkDetailSerializerTest(homework).data,
            content_type="application/json"
        )
        
        self.assertStatusOk(response.status_code)
        
        self.assertTrue(Homework.objects.all().exists())
    
    def test_update_user_homework(self):
        homework = self.Create_homework()
        new_information = lorem.sentence()
        
        response = self.client.patch(
            f"/api/data/homework/{homework.id}/",
            {
                "information": new_information
            },
            content_type="application/json"
        )
        
        self.assertStatusOk(response.status_code)
        
        homework.refresh_from_db(fields=["information"])
        self.assertEqual(homework.information, new_information)
    
    def test_filtering_relation(self):
        homework = self.Create_homework()
        completed_homework = self.Create_homework()
        
        relation = completed_homework.user_relations.get(user=self.logged_user)
        relation.completed = True
        relation.save()
        
        response = self.client.get(f"/api/data/homework/", {
            "completed": False
        }, content_type="application/json")
        expected = Homework.objects.from_user(self.logged_user).filter(userhomeworkrelation__completed=False).distinct()
        
        self.assertStatusOk(response.status_code)
        
        response = self.client.get(f"/api/data/homework/", {
            "completed": True
        }, content_type="application/json")
        expected = Homework.objects.from_user(self.logged_user).filter(userhomeworkrelation__completed=True).distinct()
        
        self.assertStatusOk(response.status_code)
    
    def test_private_homework(self):
        first_user = self.logged_user
        second_user = self.Create_user()
        
        course = self.Create_course()
        course.participants.add(first_user, second_user)
        course.save()
        
        # Public homework
        self.Create_homework(
            lesson=self.Create_lesson(
                course=course
            )
        )
        
        # Public homework, that will be added via post
        homework = self.Create_homework(
            lesson=self.Create_lesson(
                course=course
            )
        )
        homework.delete()
        
        self.client.post(
            f"/api/data/homework/",
            HomeworkDetailSerializerTest(homework).data,
            content_type="application/json"
        )
        
        # Private homework
        private_homework = self.Create_homework(
            lesson=self.Create_lesson(
                course=course
            ),
            private_to_user=first_user,
        )
        private_homework.delete()
        
        self.client.logout()
        with self.Login_user_as_context(first_user):
            self.client.post(
                f"/api/data/homework/",
                HomeworkDetailSerializerTest(private_homework).data,
                content_type="application/json"
            )
        
        private_homework = Homework.objects.get(private_to_user=first_user)
        
        # Check
        
        # Should return public + private
        with self.Login_user_as_context(first_user):
            response = self.client.get(f"/api/data/homework/")
            homeworks = Homework.objects.from_user(first_user).distinct()
            
            self.assertStatusOk(response.status_code)
            self.assertIn(private_homework, homeworks)
        
        # Should return only public
        with self.Login_user_as_context(second_user):
            response = self.client.get(f"/api/data/homework/")
            homeworks = Homework.objects.from_user(second_user).distinct()
            
            self.assertStatusOk(response.status_code)
            self.assertNotIn(private_homework, homeworks)
    
    def test_information(self):
        for _ in range(5):
            self.Create_homework()
        
        response = self.client.get(f"/api/data/homework/homework-information/")
        
        self.assertStatusOk(response.status_code)
        pp(response.data)
    
    def test_delete_list(self):
        DELETE_AMOUNT = 3
        
        for _ in range(10):
            self.Create_homework(private_to_user=self.__class__.associated_user)
        
        homework_ids = random.choices(Homework.objects.all().values_list("id", flat=True).distinct(), k=DELETE_AMOUNT)
        
        response = self.client.delete("/api/data/homework/", {
            "ids": homework_ids
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
        self.assertEqual(Homework.objects.all().count(), 10 - DELETE_AMOUNT)
        print(response.data)
        
        random_id = random.choice(Homework.objects.all().values_list('id', flat=True).distinct())
        response = self.client.delete(f"/api/data/homework/{random_id}/")
        self.assertStatusOk(response.status_code)
        self.assertEqual(Homework.objects.all().count(), 10 - DELETE_AMOUNT - 1)
        print(response.data)


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
