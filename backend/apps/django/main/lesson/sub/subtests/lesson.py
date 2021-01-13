from apps.django.main.lesson.mixins.tests import *
from apps.django.main.lesson.mixins.tests.associated_user import *
from apps.django.main.lesson.models import *
from apps.django.utils.tests import *

__all__ = [
    "QuerySetTest"
]


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
    
    def count(self) -> int:
        return UserLessonRelation.objects.all().count()
    
    def test_relation_count(self):
        self.assertEqual(self.count(), 0)
        
        lesson = Lesson.objects.first()
        
        response = self.client.patch(
            f"/api/user-relation/lesson/{lesson.id}/",
            {
                "attendance": False
            },
            content_type="application/json"
        )
        self.assertStatusOk(response.status_code)
        self.assertEqual(response.data["attendance"], False)
        self.assertEqual(self.count(), 1)
        
        response = self.client.patch(
            f"/api/user-relation/lesson/{lesson.id}/",
            {
                "attendance": True
            },
            content_type="application/json"
        )
        self.assertStatusOk(response.status_code)
        self.assertEqual(response.data["attendance"], True)
        self.assertEqual(self.count(), 1)
