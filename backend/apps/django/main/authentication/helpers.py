from typing import *

from django.conf import settings
from django.core.mail import send_mail

if TYPE_CHECKING:
    from .models import User

__all__ = [
    "send_email_verification"
]


def send_email_verification(user: "User") -> None:
    url = "https://tabool.app/app/auth/registration/email/" + user.confirmation_key + "/"
    
    message = f"""
    Hi {user.first_name}!

    Du kannst deine E-Mail bestätigen, indem du einfach auf diesen Link drückst:

    {url}
    """
    
    send_mail(
        "Bestätige deine E-Mail",
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
