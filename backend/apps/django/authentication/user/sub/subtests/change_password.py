from apps.django.authentication.user.mixins import UserTestMixin


class ChangePasswordSerializer(UserTestMixin):
    def setUp(self):
        self.password = "asd6SDc645v54asdSADasw§2134dsgSdaSD"
        self.user = self.Create_student_user(password=self.password)
        self.Login_user(self.user, self.password)
    
    def test_changes_when_correct(self):
        response = self.client.post("/api/auth/change-password/", {
            "old_password": self.password,
            "new_password": "qweQWE123!!%%"
        })
        self.assertStatusOk(response.status_code)
    
    def test_does_not_change_when_not_correct(self):
        response = self.client.post("/api/auth/change-password/", {
            "old_password": "a",
            "new_password": "qweQWE123!!%%"
        })
        self.assertStatusNotOk(response.status_code)
    
    def test_does_not_change_when_not_new_is_same_as_old(self):
        response = self.client.post("/api/auth/change-password/", {
            "old_password": self.password,
            "new_password": self.password
        })
        self.assertStatusNotOk(response.status_code)
