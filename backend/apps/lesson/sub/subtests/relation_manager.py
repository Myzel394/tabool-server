from apps.lesson.mixins.tests import LessonTestMixin
from apps.lesson.models import UserLessonRelation
from apps.utils import ClientTestMixin, UserTestMixin


class RelationTest(ClientTestMixin, LessonTestMixin, UserTestMixin):
    def test_user_created_after_object_created(self):
        with self.Login_user_as_context() as user:
            self.__class__.associated_user = user
            
            self.Create_lesson()
            before_create_count = UserLessonRelation.objects.all().count()
            self.assertEqual(before_create_count, 1)
