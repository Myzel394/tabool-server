from typing import *

from django.conf import settings
from django.core.mail import send_mail

if TYPE_CHECKING:
    from .models import User

__all__ = [
    "send_email_verification"
]


def send_email_verification(user: "User") -> None:
    # TODO: Better solution!
    message = f"""
    Hi {user.first_name}!

    Du kannst deine E-Mail bestätigen, indem du diesen Code kopierst und ihn in der App eingibst.
    Hier dein Bestätigungscode:

    {user.confirmation_key}
    """
    
    send_mail(
        "Bestätige deine E-Mail",
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
