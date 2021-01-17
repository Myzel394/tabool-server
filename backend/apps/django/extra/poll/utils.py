from typing import *

from .models import Poll, Vote

if TYPE_CHECKING:
    from .models import Choice
    from apps.django.main.authentication.models import User

__all__ = [
    "has_voted", "add_user_vote"
]


def has_voted(poll: Poll, user: "User") -> bool:
    return Vote.objects \
        .only("poll", "associated_user") \
        .filter(poll=poll, associated_user=user) \
        .exists()


def add_user_vote(poll: Poll, user: "User", choices: list["Choice"]) -> None:
    if not has_voted(poll, user):
        vote = Vote.objects.create(
            poll=poll,
            associated_user=user,
        )
        vote.choices.add(*choices)
