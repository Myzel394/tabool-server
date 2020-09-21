import json

from apps.homework.mixins.tests.homework import HomeworkTestMixin
from apps.homework.models import TeacherHomework, UserHomework
from apps.homework.sub.subserializers import TeacherHomeworkSerializer, UserHomeworkSerializer
from apps.utils.tests import ClientTestMixin


class APITest(HomeworkTestMixin, ClientTestMixin):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
    
    def test_receive_from_lesson(self):
        homework = self.Create_teacher_homework(
            lesson=self.Create_lesson(associated_user=self.logged_user)
        )
        
        response = self.client.get(
            "/api/teacher-homework/"
        )
        
        self.assertEqual(
            json.loads(json.dumps(response.data)),
            json.loads(json.dumps(TeacherHomeworkSerializer(TeacherHomework.objects.all(), many=True).data))
        )
    
    def test_create_user_homework(self):
        homework = self.Create_user_homework()
        homework.delete()
        
        response = self.client.post(
            "/api/user-homework/",
            UserHomeworkSerializer(homework).data,
            content_type="application/json"
        )
        
        print(UserHomework.objects.all())
        
        self.assertTrue(UserHomework.objects.all().exists())
