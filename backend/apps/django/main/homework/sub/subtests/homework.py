from pprint import pp

import lorem

from apps.django.main.homework.mixins.tests import HomeworkTestMixin
from apps.django.main.homework.models import Homework
from apps.django.main.homework.serializers import *
from apps.django.main.homework.sub.subserializers.tests import *
from apps.django.main.lesson.mixins.tests import *
from apps.django.utils.tests import ClientTestMixin

__all__ = [
    "APITest", "QuerySetTest"
]

from constants.api import API_VERSION


class APITest(HomeworkTestMixin, ClientTestMixin):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
        self.__class__.associated_user = self.logged_user
    
    def test_receive(self):
        homework = self.Create_homework()
        
        response = self.client.get(f"/api/{API_VERSION}/data/homework/")
        
        self.assertStatusOk(response.status_code)
        
        self.assertCountEqual(
            response.data["results"],
            HomeworkListSerializer(
                Homework.objects.from_user(self.logged_user),
                many=True
            ).data
        )
    
    def test_create_user_homework(self):
        homework = self.Create_homework()
        homework.delete()
        
        response = self.client.post(
            f"/api/{API_VERSION}/data/homework/",
            HomeworkDetailSerializerTest(homework).data,
            content_type="application/json"
        )
        
        self.assertStatusOk(response.status_code)
        
        self.assertTrue(Homework.objects.all().exists())
    
    def test_update_user_homework(self):
        homework = self.Create_homework()
        new_information = lorem.sentence()
        
        response = self.client.patch(
            f"/api/{API_VERSION}/data/homework/{homework.id}/",
            {
                "information": new_information
            },
            content_type="application/json"
        )
        
        self.assertStatusOk(response.status_code)
        
        homework.refresh_from_db(fields=["information"])
        self.assertEqual(homework.information, new_information)
    
    def test_filtering(self):
        lesson = self.Create_lesson()
        self.Create_homework(
            lesson=lesson
        )
        
        response = self.client.get(f"/api/{API_VERSION}/data/homework/", {
            "lesson": lesson.scooso_id
        }, content_type="application/json")
        
        self.assertStatusOk(response.status_code)
        
        expected_homeworks = Homework \
            .objects \
            .all() \
            .from_user(self.logged_user) \
            .filter(lesson__id=lesson.scooso_id)
        expected_data = HomeworkListSerializer(expected_homeworks, many=True).data
        actual_data = response.data["results"]
        
        self.assertCountEqual(actual_data, expected_data)
    
    def test_filtering_relation(self):
        homework = self.Create_homework()
        completed_homework = self.Create_homework()
        
        relation = completed_homework.user_relations.get(user=self.logged_user)
        relation.completed = True
        relation.save()
        
        response = self.client.get(f"/api/{API_VERSION}/data/homework/", {
            "completed": False
        }, content_type="application/json")
        expected = Homework.objects.from_user(self.logged_user).filter(userhomeworkrelation__completed=False).distinct()
        
        self.assertStatusOk(response.status_code)
        self.assertCountEqual(
            response.data["results"],
            HomeworkListSerializer(expected, many=True).data
        )
        
        response = self.client.get(f"/api/{API_VERSION}/data/homework/", {
            "completed": True
        }, content_type="application/json")
        expected = Homework.objects.from_user(self.logged_user).filter(userhomeworkrelation__completed=True).distinct()
        
        self.assertStatusOk(response.status_code)
        self.assertCountEqual(
            response.data["results"],
            HomeworkListSerializer(expected, many=True).data
        )
    
    def test_private_homework(self):
        first_user = self.logged_user
        second_user = self.Create_user()
        
        course = self.Create_course()
        course.participants.add(first_user, second_user)
        course.save()
        
        # Public homework
        self.Create_homework(
            lesson=self.Create_lesson(
                lesson_data=self.Create_lesson_data(
                    course=course
                )
            )
        )
        
        # Public homework, that will be added via post
        homework = self.Create_homework(
            lesson=self.Create_lesson(
                lesson_data=self.Create_lesson_data(
                    course=course
                )
            )
        )
        homework.delete()
        
        self.client.post(
            f"/api/{API_VERSION}/data/homework/",
            HomeworkDetailSerializerTest(homework).data,
            content_type="application/json"
        )
        
        # Private homework
        private_homework = self.Create_homework(
            lesson=self.Create_lesson(
                lesson_data=self.Create_lesson_data(
                    course=course
                )
            ),
            private_to_user=first_user,
        )
        private_homework.delete()
        
        self.client.logout()
        with self.Login_user_as_context(first_user):
            self.client.post(
                f"/api/{API_VERSION}/data/homework/",
                HomeworkDetailSerializerTest(private_homework).data,
                content_type="application/json"
            )
        
        private_homework = Homework.objects.get(private_to_user=first_user)
        
        # Check
        
        # Should return public + private
        with self.Login_user_as_context(first_user):
            response = self.client.get(f"/api/{API_VERSION}/data/homework/")
            homeworks = Homework.objects.from_user(first_user).distinct()
            
            self.assertStatusOk(response.status_code)
            self.assertCountEqual(
                HomeworkListSerializer(homeworks, many=True).data,
                response.data["results"]
            )
            self.assertIn(private_homework, homeworks)
        
        # Should return only public
        with self.Login_user_as_context(second_user):
            response = self.client.get(f"/api/{API_VERSION}/data/homework/")
            homeworks = Homework.objects.from_user(second_user).distinct()
            
            self.assertStatusOk(response.status_code)
            self.assertCountEqual(
                HomeworkListSerializer(homeworks, many=True).data,
                response.data["results"]
            )
            self.assertNotIn(private_homework, homeworks)
    
    def test_homework_relation(self):
        homework = self.Create_homework()
        
        response = self.client.get(f"/api/{API_VERSION}/data/homework/{homework.id}/")
        data = response.data
        pp(data)


class QuerySetTest(HomeworkTestMixin, AssociatedUserTestMixin):
    def test_association(self):
        self.check_queryset_from_user(Homework)