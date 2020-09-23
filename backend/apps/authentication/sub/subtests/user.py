import names
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.authentication.models import AccessToken
from apps.utils.tests import ClientTestMixin, UserCreationTestMixin


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
        self.Login_user()
        access_token: AccessToken = AccessToken.objects.create()
        
        # Simple creation check
        self.client.post("/api/authentication/registration/", {
            "first_name": names.get_first_name(),
            "last_name": names.get_last_name(),
            "password": names.get_first_name(),
            "email": f"{names.get_first_name()}@gmail.com",
            "token": access_token.token
        }, content_type="application/json")
        
        self.client.post("/api/authentication/registration/", {
            "first_name": names.get_first_name(),
            "last_name": names.get_last_name(),
            "password": names.get_first_name(),
            "email": f"{names.get_first_name()}@gmail.com",
            "token": "a" * AccessToken.TOKEN_LENGTH
        }, content_type="application/json")
        
        # Double token check
        with self.assertRaises(serializers.ValidationError):
            self.client.post("/api/authentication/registration/", {
                "first_name": names.get_first_name(),
                "last_name": names.get_last_name(),
                "password": names.get_first_name(),
                "email": f"{names.get_first_name()}@gmail.com",
                "token": "a" * AccessToken.TOKEN_LENGTH
            }, content_type="application/json")
        
        # No token check
        with self.assertRaises(ValidationError):
            self.client.post("/api/authentication/registration/", {
                "first_name": names.get_first_name(),
                "last_name": names.get_last_name(),
                "password": names.get_first_name(),
                "email": f"{names.get_first_name()}@gmail.com",
            }, content_type="application/json")
    
    def test_forgot_password(self):
        password = "awesome_password"
        
        user = self.Create_user(
            password=password
        )
        
        self.Login_user(user, password)
        
        self.client.post("/api/authentication/change-password/", {
            "old_password": password,
            "new_password": password + "abc",
            "user": user.id
        }, content_type="application/json")
        
        with self.assertRaises(ValidationError):
            self.client.post("/api/authentication/change-password/", {
                "old_password": password + "abc",
                "new_password": password,
                "user": user.id
            }, content_type="application/json")
