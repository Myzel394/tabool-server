from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from apps.authentication.mixins.tests import UserPaymentTestMixin
from apps.authentication.models import UserPayment
from apps.utils import ClientTestMixin
from apps.utils.perms import perm_to_permission
from ... import constants

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
            f"/api/user-payment/"
        )
        self.assertEqual(response.status_code, 403)
        
        # Not owner
        response = self.client.get(
            f"/api/user-payment/{self.not_pay_user.id}/"
        )
        self.assertEqual(response.status_code, 404)
        
        # Owner
        response = self.client.get(
            f"/api/user-payment/{self.logged_user.payments[0].id}/"
        )
        self.assertStatusOk(response.status_code)
        
    def test_patch_not_ok(self):
        # Owner patch check, should not work
        response = self.client.patch(
            f"/api/user-payment/{self.logged_user.payments[0].id}/"
        )
        self.assertStatusNotOk(response.status_code)
    

class TestPrivileged(ClientTestMixin, UserPaymentTestMixin):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
        self.Create_user_payment(user=self.logged_user)
        
        for _ in range(5):
            self.Create_user_payment()
        
        self.not_pay_user = self.Create_user()
        
        # At end, because `Create_user_payment` would otherwise associated it
        self.__class__.associated_user = self.logged_user
        
        model = UserPayment
        all_perms = [
            perm
            for perm in Permission.objects.all()
        ]
        
        # Add privileges
        self.logged_user.user_permissions.add(
            perm_to_permission(f"{constants.APP_LABEL}.change_userpayment"),
            perm_to_permission(f"{constants.APP_LABEL}.view_userpayment")
        )
        self.logged_user.save()
    
    def test_access(self):
        # List access
        response = self.client.get(
            f"/api/user-payment/"
        )
        self.assertStatusOk(response.status_code)
    
    def test_patch(self):
        payment = UserPayment.objects.all().first()
        
        response = self.client.patch(
            f"/api/user-payment/{payment.id}/",
            {
                "has_paid": True,
            }
        )
        self.assertStatusOk(response.status_code)
        self.assertEqual(payment, True)
