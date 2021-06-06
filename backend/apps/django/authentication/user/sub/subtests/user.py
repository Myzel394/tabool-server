from apps.django.authentication.user.mixins import UserTestMixin


class UserAPITest(UserTestMixin):
    def setUp(self):
        self.student = self.Login_student()

    def test_get(self):
        response = self.client.get(f"/api/student/user/{self.student.id}/")
        self.assertStatusOk(response.status_code)
