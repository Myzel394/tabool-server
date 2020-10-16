from apps.django.main.authentication.models import UserPayment
from apps.django.utils.tests import *

__all__ = [
    "UserPaymentTestMixin"
]


class UserPaymentTestMixin(UserTestMixin):
    def Create_user_payment(self, **kwargs):
        return UserPayment.objects.create(
            **joinkwargs(
                {
                    "user": self.Create_user,
                },
                kwargs
            )
        )
