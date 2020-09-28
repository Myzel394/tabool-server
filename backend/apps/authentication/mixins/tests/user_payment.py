from apps.authentication.models import UserPayment
from apps.utils import joinkwargs, UserCreationTestMixin

__all__ = [
    "UserPaymentTestMixin"
]


class UserPaymentTestMixin(UserCreationTestMixin):
    @classmethod
    def Create_user_payment(cls, **kwargs):
        return UserPayment.objects.create(
            **joinkwargs(
                {
                    "user": cls.Create_user,
                },
                kwargs
            )
        )
    

