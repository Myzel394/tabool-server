import random
import string
from datetime import datetime, timedelta

from apps.django.authentication.otp.models import OTP
from apps.django.authentication.user.mixins import UserTestMixin


class AuthenticationOTPTest(UserTestMixin):
    def setUp(self) -> None:
        self.user_password = self.Get_random_password()
        
        self.user = self.Create_student_user(password=self.user_password)
    
    def request(self) -> OTP:
        response = self.client.post("/api/auth/login/", {
            "email": self.user.email,
            "password": self.user_password
        }, content_type="application/json")
        
        self.assertEqual(401, response.status_code)
        
        otp = OTP.objects.all().first()
        
        return otp
    
    def test_otp_valid(self):
        otp = self.request()
        
        response = self.client.post("/api/auth/login/", {
            "email": self.user.email,
            "password": self.user_password,
            "otp_key": otp.token
        }, content_type="application/json")
        
        self.assertStatusOk(response.status_code)
    
    def test_otp_invalid(self):
        self.request()
        
        response = self.client.post("/api/auth/login/", {
            "email": self.user.email,
            "password": self.user_password,
            "otp_key": "".join(random.choices(string.ascii_letters + string.digits, k=OTP.TOKEN_LENGTH))
        }, content_type="application/json")
        
        self.assertStatusNotOk(response.status_code)
        self.assertEqual("Ungültiges OTP.", response.data["otp_key"])
    
    def test_otp_valid_expired(self):
        otp = self.request()
        
        # Make otp expired
        otp.expire_date = datetime.now() - timedelta(days=20)
        otp.save()
        
        response = self.client.post("/api/auth/login/", {
            "email": self.user.email,
            "password": self.user_password,
            "otp_key": otp.token
        }, content_type="application/json")
        
        self.assertStatusNotOk(response.status_code)
        self.assertEqual("Dieses OTP ist abgelaufen. Es wurde dir ein neues zugeschickt.", response.data["otp_key"])
    
    def test_otp_not_existing(self):
        response = self.client.post("/api/auth/login/", {
            "email": self.user.email,
            "password": self.user_password,
            "otp_key": "123456"
        }, content_type="application/json")
        
        self.assertEqual(401, response.status_code)
    
    def test_otp_deletes_after_success(self):
        otp = self.request()
        
        response = self.client.post("/api/auth/login/", {
            "email": self.user.email,
            "password": self.user_password,
            "otp_key": otp.token
        }, content_type="application/json")
        
        self.assertStatusOk(response.status_code)
        
        new_otp = self.request()
        self.assertNotEqual(otp, new_otp)
    
    def test_no_new_otp_created_after_wrong_input(self):
        otp = self.request()
        
        response = self.client.post("/api/auth/login/", {
            "email": self.user.email,
            "password": self.user_password,
            "otp_key": "123456"
        }, content_type="application/json")
        
        self.assertStatusNotOk(response.status_code)
        
        self.assertEqual(1, OTP.objects.all().count())
        
        response = self.client.post("/api/auth/login/", {
            "email": self.user.email,
            "password": self.user_password,
            "otp_key": otp.token
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
