from apps.django.main.lesson.mixins.tests import *
from apps.django.main.lesson.models import *
from apps.django.utils.tests import *


class RelationTest(ClientTestMixin, LessonTestMixin, UserTestMixin):
    def test_user_created_after_object_created(self):
        with self.Login_user_as_context() as user:
            self.__class__.associated_user = user
            
            self.Create_lesson()
            before_create_count = UserLessonRelation.objects.all().count()
            self.assertEqual(before_create_count, 1)
