from apps.lesson.mixins.tests import LessonTestMixin
from apps.lesson.mixins.tests.associated_user import AssociatedUserTestMixin
from apps.lesson.models import Course, Lesson
from apps.utils.tests import ClientTestMixin, UserCreationTestMixin

__all__ = [
    "QuerySetTest"
]


class QuerySetTest(LessonTestMixin, AssociatedUserTestMixin):
    def test_association(self):
        self.check_queryset_from_user(Lesson)
        self.check_queryset_from_user(Course)


class UserRelationTest(LessonTestMixin, ClientTestMixin, UserCreationTestMixin):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
        self.__class__.associated_user = self.logged_user
        
        for _ in range(20):
            self.Create_lesson()
    
    def test_relation(self):
        lesson = Lesson.objects.all().first()
        
        response = self.client.get(f"/api/lesson/user-relation/{lesson.id}/")
        
        self.assertStatusOk(response.status_code)
        self.assertTrue(response.data["attendance"])
        
        self.client.patch(
            f"/api/lesson/user-relation/{lesson.id}/",
            {
                "attendance": False
            },
            content_type="application/json"
        )
        
        response = self.client.get(f"/api/lesson/user-relation/{lesson.id}/")
        
        self.assertStatusOk(response.status_code)
        self.assertFalse(response.data["attendance"])
        
        # Check whether other lessons weren't affected
        
        other_lesson = Lesson.objects.all().last()
        response = self.client.get(f"/api/lesson/user-relation/{other_lesson.id}/")
        
        self.assertStatusOk(response.status_code)
        self.assertTrue(response.data["attendance"])
