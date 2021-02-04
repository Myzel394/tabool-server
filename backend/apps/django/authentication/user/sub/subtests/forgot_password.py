from django_rest_passwordreset.models import ResetPasswordToken

from apps.django.utils.tests_mixins import ClientTestMixin, UserTestMixin


class ForgotPasswordTest(UserTestMixin, ClientTestMixin):
    def setUp(self):
        self.user = self.Login_user()
        self.__class__.associated_user = self.user
    
    def request(self) -> None:
        response = self.client.post("/api/auth/reset-password/", {
            "email": self.user.email
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
    
    def test_valid_token(self):
        self.request()
        
        token = ResetPasswordToken.objects.all()[0]
        
        response = self.client.post("/api/auth/reset-password/confirm/", {
            "password": self.Get_random_password(),
            "token": token.key,
            "email": self.user.email
        })
        self.assertStatusOk(response.status_code)
    
    def test_invalid_token(self):
        self.request()
        
        response = self.client.post("/api/auth/reset_password/confirm/", {
            "password": self.Get_random_password(),
            "token": "asdf",
            "email": self.user.email
        })
        self.assertStatusNotOk(response.status_code)
