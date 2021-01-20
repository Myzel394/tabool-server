import random

import names

from apps.django.extra.scooso_scraper.mixins.tests import DummyUser
from apps.django.main.authentication.models import *
from apps.django.main.school_data.mixins.tests import *
from apps.django.utils.tests import *
from ... import constants


class RegistrationTest(ClientTestMixin, TeacherTestMixin, UserTestMixin, DummyUser):
    def setUp(self) -> None:
        self.load_dummy_user()
    
    def create_scooso_data(self) -> dict:
        return {
            "username": self.username,
            "password": self.password
        }
    
    def create_student_data(self) -> dict:
        return {
            "main_teacher": self.Create_teacher().id,
            "class_number": random.randint(
                constants.AVAILABLE_CLASS_NUMBERS.start,
                constants.AVAILABLE_CLASS_NUMBERS.stop - 1
            )
        }
    
    def test_create_user_full(self):
        print("Creating user")
        
        # Step 1 Token
        print("Step 1, Token")
        token = Token.objects.create()
        
        # Step 2 Simple registration
        print("Step 2, Simple registration")
        password = self.Get_random_password()
        email = f"{names.get_first_name()}@gmail.com"
        
        response = self.client.post(f"/api/auth/registration/", {
            "email": email,
            "password": password,
            "token": token.token
        }, content_type="application/json")
        
        # Check
        self.assertStatusOk(response.status_code)
        User.objects.get(email__iexact=email)
        
        # Step 3, Email
        print("Step 3, email verification")
        user = User.objects.all().first()
        user.confirm_email(user.confirmation_key)
        
        # Step 4, Fill out data
        print("Step 4, Fill out data")
        scooso_data = self.create_scooso_data()
        student_data = self.create_student_data()
        
        response = self.client.post(f"/api/auth/full-registration/", {
            "scoosodata": scooso_data,
            "student": student_data,
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
    
    def test_user_cant_register_two_times(self):
        email = f"{names.get_first_name()}@gmail.com"
        password = self.Get_random_password()
        
        self.Create_user(
            is_confirmed=False,
            create_scooso_data=False,
            email=email,
            password=password,
        )
        response = self.client.post(f"/api/auth/registration/", {
            "email": email,
            "password": password,
            "token": Token.objects.create().token
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)
    
    def test_user_cant_fill_out_twice(self):
        email = f"{names.get_first_name()}@gmail.com"
        password = self.Get_random_password()
        self.Create_user(
            is_confirmed=True,
            create_scooso_data=False,
            email=email,
            password=password
        )
        
        scooso_data = self.create_scooso_data()
        student_data = self.create_student_data()
        
        response = self.client.post(f"/api/auth/full-registration/", {
            "scoosodata": scooso_data,
            "student": student_data,
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)
