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
    
    def test_deactivated_account(self):
        self.user.is_active = False
        self.user.save()
        
        response = self.client.post("/api/auth/login/", {
            "email": self.user.email,
            "password": self.password
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)


class AuthenticationInformationResponseTest(UserTestMixin):
    def setUp(self):
        self.password = "asgEIUA!!ew423gwov345jö"
    
    def request(self, data=None):
        data = data or {
            "email": self.user.email,
            "password": self.password
        }
        
        self.client.post("/api/auth/login/", data, content_type="application/json")
        otp: OTP = OTP.objects.all()[0]
        response = self.client.post("/api/auth/login/", {
            **data,
            "otp_key": otp.token,
        }, content_type="application/json")
        
        return response
    
    def test_student(self):
        self.user = self.Create_student_user(password=self.password)
        
        response = self.request()
        self.assertStatusOk(response.status_code)
        self.assertIsNotNone(response.data["student"])
        self.assertIsNone(response.data["teacher"])
    
    def test_teacher(self):
        self.user = self.Create_teacher_user(password=self.password)
        
        response = self.request()
        self.assertStatusOk(response.status_code)
        self.assertIsNone(response.data["student"])
        self.assertIsNotNone(response.data["teacher"])
