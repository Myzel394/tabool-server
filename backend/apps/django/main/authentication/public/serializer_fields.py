from apps.django.utils.serializers import WritableAllFieldMixin, WritableFromUserFieldMixin
from ..models import AccessToken, ScoosoData, User, UserPayment

__all__ = [
    "AccessTokenField", "UserPaymentField", "ScoosoDataField", "UserField"
]


class AccessTokenField(WritableFromUserFieldMixin):
    model = AccessToken


class UserPaymentField(WritableFromUserFieldMixin):
    model = UserPayment


class ScoosoDataField(WritableFromUserFieldMixin):
    model = ScoosoData


# TODO: Check UserField!
class UserField(WritableAllFieldMixin):
    model = User
