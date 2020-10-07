from typing import *

from django.conf import settings
from django.core.mail import send_mail

if TYPE_CHECKING:
    from .models import User
    

__all__ = [
    "send_email_verification"
]


def send_email_verification(user: "User") -> None:
    send_mail(
        "Bestätige deine E-Mail",
        "",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    # TODO: Add!
