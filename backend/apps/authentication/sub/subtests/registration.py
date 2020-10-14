import random

from apps.authentication.models import AccessToken, User
from apps.authentication.models.student import Student
from apps.school_data.mixins.tests import TeacherTestMixin
from apps.utils import ClientTestMixin, UserTestMixin
from project.urls import API_VERSION
from ... import constants


class RegistrationTest(ClientTestMixin, TeacherTestMixin, UserTestMixin):
    def test_registration(self):
        token: AccessToken = AccessToken.objects.create()
        email = "mail@gmail.com"
        password = self.Get_random_password()
        
        response = self.client.post(
            f"/api/{API_VERSION}/auth/registration/",
            {
                "token": token.token,
                "email": email,
                "password": password
            }
        )
        self.assertStatusOk(response.status_code)
        self.assertEqual(User.objects.all().count(), 1)
        user = User.objects.all().first()
        
        teacher = self.Create_teacher()
        student_kwargs = {
            "main_teacher": teacher.id,
            "class_number": random.choice(constants.AVAILABLE_CLASS_NUMBERS)
        }
        
        response = self.client.post(
            f"/api/{API_VERSION}/api/auth/student/",
            student_kwargs,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        
        user.is_email_verified = True
        user.save()
        
        response = self.client.post(
            f"/api/auth/student/",
            student_kwargs,
            content_type="application/json"
        )
        self.assertStatusOk(response.status_code)
        
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(Student.objects.all().count(), 1)
        
        response = self.client.post(
            f"/api/{API_VERSION}/auth/student/",
            student_kwargs,
            content_type="application/json"
        )
        self.assertStatusNotOk(response.status_code)
