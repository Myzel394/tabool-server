from apps.utils.serializers import WritableFromUserFieldMixin, WritableAllFieldMixin
from ..models import User, AccessToken, UserPayment, ScoosoData


__all__ = [
    "AccessTokenField", "UserPaymentField", "ScoosoDataField", "UserField"
]


class AccessTokenField(WritableFromUserFieldMixin):
    model = AccessToken


class UserPaymentField(WritableFromUserFieldMixin):
    model = UserPayment


class ScoosoDataField(WritableFromUserFieldMixin):
    model = ScoosoData


class UserField(WritableAllFieldMixin):
    model = User
