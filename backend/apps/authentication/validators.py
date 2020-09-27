from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import AccessToken

User = get_user_model()

__all__ = [
    "token_exists", "token_not_in_use", "email_not_in_use"
]


def token_exists(value: str):
    if not AccessToken.objects.all().only("token").filter(token=value).exists():
        raise ValidationError(_("Zugangscode nicht gültig"))


def token_not_in_use(value: str):
    if AccessToken.objects.all().only("token", "user").filter(token=value).exclude(user=None).exists():
        raise ValidationError(
            _("Dieser Zugangscode wurde bereits verwendet. Du kannst Zugangscode nur für einen Account "
              "verwenden. Wenn dein Zugangscode von jemand anderem verwendet wurde, kontaktiere uns.")
        )


def email_not_in_use(value: str):
    if User.objects.all().only("email").filter(email__iexact=value).exists():
        raise ValidationError(
            _("Diese E-Mail wurde bereits registriert.")
        )
