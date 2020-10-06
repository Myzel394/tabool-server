from typing import *

if TYPE_CHECKING:
    from .models import User


def send_email_verification(user: "User") -> None:
    pass
