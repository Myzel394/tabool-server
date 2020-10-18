from django.contrib.auth import get_user_model

from apps.django.main.authentication.mixins.tests import UserPaymentTestMixin
from apps.django.utils.tests import *

User = get_user_model()


class TestNotPrivileged(ClientTestMixin, UserPaymentTestMixin):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
        self.Create_user_payment(user=self.logged_user)
        
        for _ in range(5):
            self.Create_user_payment()
        
        self.not_pay_user = self.Create_user()
        
        # At end, because `Create_user_payment` would otherwise associated it
        self.__class__.associated_user = self.logged_user
    
    def test_access(self):
        # List access
        response = self.client.get(
            f"/api/data/user-payment/"
        )
        self.assertEqual(response.status_code, 404)
        
        # Not owner
        response = self.client.get(
            f"/api/data/user-payment/{self.not_pay_user.id}/"
        )
        self.assertEqual(response.status_code, 404)
        
        # Owner
        response = self.client.get(
            f"/api/data/user-payment/{self.logged_user.payments[0].id}/"
        )
        self.assertStatusOk(response.status_code)
