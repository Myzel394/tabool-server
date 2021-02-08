from apps.django.authentication.otp.models import OTP
from apps.django.authentication.user.mixins import UserTestMixin


class AuthenticationTest(UserTestMixin):
    def setUp(self):
        self.password = "asgEIUA!!ew423gwov345jö"
        self.user = self.Create_student_user(password=self.password)
    
    def request(self, data):
        self.client.post("/api/auth/login/", data, content_type="application/json")
        otp: OTP = OTP.objects.all()[0]
        response = self.client.post("/api/auth/login/", {
            **data,
            "otp_key": otp.token,
        }, content_type="application/json")
        
        return response
    
    def test_correct(self):
        response = self.request({
            "email": self.user.email,
            "password": self.password
        })
        self.assertStatusOk(response.status_code)
    
    def test_invalid_email(self):
        response = self.client.post("/api/auth/login/", {
            "email": self.user.email + "aaa",
            "password": self.password
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)
    
    def test_invalid_password(self):
        response = self.client.post("/api/auth/login/", {
            "email": self.user.email,
            "password": self.password + "aaa"
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)
