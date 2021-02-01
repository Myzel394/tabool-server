import random

from apps.django.main.school_data.mixins.tests import TeacherTestMixin
from apps.django.main.school_data.models import Teacher
from apps.django.utils.tests_mixins import ClientTestMixin, UserTestMixin


class TeacherAPITest(TeacherTestMixin, ClientTestMixin, UserTestMixin):
    def setUp(self) -> None:
        self.user = self.Login_user()
        self.__class__.associated_user = self.user
        
        for _ in range(10):
            self.Create_teacher()
    
    @staticmethod
    def get_random_teacher() -> Teacher:
        return random.choice(Teacher.objects.all())
    
    def test_get_information_succeeds(self):
        teacher = self.get_random_teacher()
        
        response = self.client.get(f"/api/data/teacher/{teacher.id}/information/")
        self.assertStatusOk(response.status_code)
