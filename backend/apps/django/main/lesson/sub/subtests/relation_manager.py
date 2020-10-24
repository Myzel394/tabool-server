from apps.django.main.lesson.mixins.tests import *
from apps.django.main.school_data.models import UserSubjectRelation
from apps.django.utils.tests import *


class RelationTest(ClientTestMixin, LessonTestMixin, UserTestMixin):
    def count(self) -> int:
        return UserSubjectRelation.objects.all().count()
    
    def test_user_created_after_object_created(self):
        self.Create_user()
        self.Create_subject()
        self.assertEqual(self.count(), 1)
        self.Create_user()
        self.assertEqual(self.count(), 2)
        self.Create_subject()
        self.assertEqual(self.count(), 4)
