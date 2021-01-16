from typing import *

from apps.django.utils.send_notification import send_notification

if TYPE_CHECKING:
    from ..models import User

__all__ = [
    "push_scooso_data_invalid"
]


def push_scooso_data_invalid(user: "User") -> None:
    send_notification(
        users=[user],
        title="Deine Scooso-Daten sind nicht mehr gültig!",
        body="Der Server konnte sich mit deinen Scooso-Daten nicht mehr anmelden. Aktualisiere bitte deine Daten.",
        collapse_group_name="scooso_data_invalid",
        is_important=True,
        data={
            "type": "scooso_data_invalid",
        }
    )
