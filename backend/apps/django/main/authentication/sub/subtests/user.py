import random
import string
import time

import names
from django.contrib.auth import get_user_model
from django.core import mail

from apps.django.extra.scooso_scraper.mixins.tests import DummyUser
from apps.django.main.authentication.models import *
from apps.django.utils.tests import *
from ... import constants

__all__ = [
    "ModelTest"
]


class ModelTest(UserTestMixin, ClientTestMixin, DummyUser):
    def setUp(self) -> None:
        self.load_dummy_user()
    
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
    
    def test_passwords(self):
        access_token: Token = Token.objects.create()
        first_name = "Josephine"
        email = f"{first_name}@gmail.com"
        default_data = {
            "email": email,
            "token": access_token.token,
            "scooso_username": names.get_first_name(),
            "scooso_password": self.Get_random_password(),
        }
        for password, is_valid in (
                ("short", False),
                ("aaaaaaaa", False),
                ("12345678", False),
                ("test1234", False),
                ("test1234!", False),
                (self.Get_random_password(), True),
        ):
            time.sleep(.5)
            print("Testing password", password)
            data = default_data | {
                "password": password
            }
            response = self.client.post(
                f"/api/auth/registration/",
                data,
                content_type="application/json"
            )
            self.assertStatusOk(response.status_code) if is_valid else self.assertStatusNotOk(response.status_code)
    
    def test_token(self):
        access_token: Token = Token.objects.create()
        password = self.Get_random_password()
        
        default_data = {
            "password": password,
            "email": f"{names.get_first_name()}@gmail.com",
            "token": access_token.token,
            "scooso_username": names.get_first_name(),
            "scooso_password": self.Get_random_password(),
        }
        # Simple creation check
        response = self.client.post(
            f"/api/auth/registration/",
            default_data,
            content_type="application/json"
        )
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
            
            response = self.client.post(
                f"/api/auth/registration/",
                use_data,
                content_type="application/json"
            )
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
            
            response = self.client.post(
                f"/api/auth/registration/",
                use_data,
                content_type="application/json"
            )
            self.assertStatusNotOk(response.status_code)
    
    def test_change_password(self):
        password = "awesome_password"
        
        user = self.Create_user(
            password=password
        )
        
        self.Login_user(user, password)
        
        response = self.client.post(f"/api/auth/change-password/", {
            "old_password": password,
            "new_password": "".join(random.choices(string.ascii_letters + string.digits, k=20)),
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
        
        response = self.client.post(f"/api/auth/change-password/", {
            "old_password": password + "abc",
            "new_password": password,
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)
    
    def test_user_email(self):
        self.Create_user()
        
        self.assertEqual(len(mail.outbox), 1)
    
    def test_email_verification(self):
        user = self.Create_user(False)
        
        with self.Login_user_as_context(user, user.first_name) as _:
            response = self.client.post(
                f"/api/auth/confirmation/",
                {
                    "confirmation_key": "a"
                },
                content_type="application/json"
            )
            self.assertStatusNotOk(response.status_code)
            user.refresh_from_db()
            self.assertEqual(user.is_confirmed, False)
            
            print(user.confirmation_key)
            
            response = self.client.post(
                f"/api/auth/confirmation/",
                {
                    "confirmation_key": user.confirmation_key
                },
                content_type="application/json"
            )
            self.assertStatusOk(response.status_code)
            user.refresh_from_db()
            self.assertEqual(user.is_confirmed, True)
    
    def test_filter_active_users(self):
        confirmed_user = self.Create_user(is_confirmed=True)
        not_confirmed_user = self.Create_user(is_confirmed=False)
        no_scooso_data = self.Create_user(create_scooso_data=False)
        
        manager = get_user_model().objects
        with_scooso_data = manager.with_scooso_data()
        active_users = with_scooso_data.active_users()
        
        confirmed_users_qs = active_users
        
        self.assertEqual(1, confirmed_users_qs.count())
        self.assertIn(confirmed_user, confirmed_users_qs)
        self.assertNotIn(not_confirmed_user, confirmed_users_qs)
        self.assertNotIn(no_scooso_data, confirmed_users_qs)
