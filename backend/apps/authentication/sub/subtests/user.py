import random
import string

import names
from django.contrib.auth import get_user_model

from apps.authentication.models import AccessToken
from apps.utils.tests import ClientTestMixin, UserCreationTestMixin
from ... import constants

__all__ = [
    "ModelTest"
]


class ModelTest(UserCreationTestMixin, ClientTestMixin):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")
    
    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)
    
    def test_token(self):
        access_token: AccessToken = AccessToken.objects.create()
        password = self.Get_random_password()
        
        default_data = {
            "password": password,
            "email": f"{names.get_first_name()}@gmail.com",
            "token": access_token.token,
            "scooso_username": names.get_first_name(),
            "scooso_password": self.Get_random_password(),
        }
        # Simple creation check
        response = self.client.post("/api/registration/", default_data, content_type="application/json")
        self.assertStatusOk(response.status_code)
        
        invalid_data = [
            # Invalid token check
            {"token": "a" * constants.TOKEN_LENGTH},
            # Double token check
            {},
            # No token check
            {"token": None}
        ]
        
        for invalid in invalid_data:
            use_data = default_data.copy()
            use_data.update(invalid)
            
            response = self.client.post("/api/registration/", use_data, content_type="application/json")
            self.assertStatusNotOk(response.status_code)
    
    def test_invalid_creation(self):
        default_data = {
            "scooso_username": "abc",
            "scooso_password": "abc"
        }
        invalid_data = [
            {"password": self.Get_random_password("weak")},
            {"email": "invalid-email.com"},
        ]
        
        for invalid in invalid_data:
            use_data = default_data.copy()
            use_data.update(invalid)
            
            response = self.client.post("/api/registration/", use_data, content_type="application/json")
            self.assertStatusNotOk(response.status_code)
    
    def test_creation(self):
        User = get_user_model()
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        password = self.Get_random_password()
        email = f"{first_name}.{last_name}@gmail.com"
        
        response = self.client.post("/api/registration/", {
            "email": email,
            "password": password,
            "scooso_username": first_name,
            "scooso_password": password,
            "token": AccessToken.objects.create().token
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
        User.objects.all().get(email__iexact=email)
    
    def test_forgot_password(self):
        password = "awesome_password"
        
        user = self.Create_user(
            password=password
        )
        
        self.Login_user(user, password)
        
        response = self.client.post("/api/change-password/", {
            "old_password": password,
            "new_password": "".join(random.choices(string.ascii_letters + string.digits, k=20)),
            "user": user.id
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
        
        response = self.client.post("/api/change-password/", {
            "old_password": password + "abc",
            "new_password": password,
            "user": user.id
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)
