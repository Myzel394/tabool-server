from pprint import pp

from apps.lesson.mixins.tests import LessonTestMixin
from apps.lesson.mixins.tests.associated_user import AssociatedUserTestMixin
from apps.lesson.models import Course, Lesson, UserLessonRelation
from apps.utils.tests import ClientTestMixin, UserTestMixin

__all__ = [
    "QuerySetTest"
]

from project.urls import API_VERSION


class QuerySetTest(LessonTestMixin, AssociatedUserTestMixin):
    def test_association(self):
        self.check_queryset_from_user(Lesson)
        self.check_queryset_from_user(Course)


class UserRelationTest(LessonTestMixin, ClientTestMixin, UserTestMixin):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
        self.__class__.associated_user = self.logged_user
        
        for _ in range(20):
            self.Create_lesson()
    
    def test_relation_api(self):
        lesson = Lesson.objects.first()
        lesson.lesson_data.course.update_relations()
        self.assertEqual(UserLessonRelation.objects.all().count(), 1)
        
        response = self.client.get(f"/api/{API_VERSION}/user-relation/lesson/{lesson.scooso_id}/")
        
        self.assertStatusOk(response.status_code)
        self.assertTrue(response.data["attendance"])
        
        self.client.patch(
            f"/api/user-relation/lesson/{lesson.scooso_id}/",
            {
                "attendance": False
            },
            content_type="application/json"
        )
        
        response = self.client.get(f"/api/{API_VERSION}/user-relation/lesson/{lesson.scooso_id}/")
        
        self.assertStatusOk(response.status_code)
        self.assertFalse(response.data["attendance"])
        
        # Check whether other lessons weren't affected
        
        other_lesson = Lesson.objects.last()
        other_lesson.lesson_data.course.update_relations()
        response = self.client.get(f"/api/{API_VERSION}/user-relation/lesson/{other_lesson.scooso_id}/")
        self.assertEqual(UserLessonRelation.objects.all().count(), 2)
        
        self.assertStatusOk(response.status_code)
        self.assertTrue(response.data["attendance"])
        
        course = lesson.lesson_data.course
        course.participants.remove(self.__class__.associated_user)
        course.save()
        
        self.assertEqual(UserLessonRelation.objects.all().count(), 1)


class UserRelationCreationTest(LessonTestMixin, ClientTestMixin, UserTestMixin):
    def test_relation(self):
        with self.Login_user_as_context() as user:
            lesson = self.Create_lesson()
            course = lesson.lesson_data.course
            course.participants.add(user)
            course.save()
            
            self.assertEqual(UserLessonRelation.objects.all().count(), 1)
            
            course.participants.remove(user)
            course.save()
            
            self.assertEqual(UserLessonRelation.objects.all().count(), 0)
    
    def test_string(self):
        print(self.Create_teacher())
        print(self.Create_room())
        print(self.Create_subject())
        print(self.Create_course())
        print(self.Create_lesson())
        print(self.Create_lesson_data())
        print(self.Create_user())


class APITest(LessonTestMixin, ClientTestMixin):
    def test_data(self):
        with self.Login_user_as_context() as user:
            for _ in range(10):
                self.Create_lesson()
            
            response = self.client.get(f"/api/{API_VERSION}/data/lesson/")
            self.assertStatusOk(response.status_code)
            
            pp(list(response.data["results"]))
            
            lesson_id = response.data["results"][0]["id"]
            
            response = self.client.get(f"/api/{API_VERSION}/data/lesson/{lesson_id}/")
            self.assertStatusOk(response.status_code)
            
            pp(dict(response.data))
