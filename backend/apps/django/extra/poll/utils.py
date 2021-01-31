from typing import *

from .models import Poll, Vote

if TYPE_CHECKING:
    from .models import Choice
    from apps.django.main.authentication.models import User

__all__ = [
    "has_voted", "add_user_vote", "get_results"
]


def has_voted(poll: Poll, user: "User") -> bool:
    return Vote.objects \
        .only("poll", "associated_user") \
        .filter(poll=poll, associated_user=user) \
        .exists()


def add_user_vote(poll: Poll, user: "User", choices: list["Choice"], feedback: str = None) -> None:
    if not has_voted(poll, user):
        vote = Vote.objects.create(
            poll=poll,
            associated_user=user,
            feedback=feedback,
        )
        vote.choices.add(*choices)


def get_results(instance: Poll, precision: int = 2):
    votes_amount = instance.votes.count()
    
    return [
        {
            "choice_id": choice.id,
            "percentage_value": round(instance.votes.filter(choices__in=[choice]).count() / max(1, votes_amount),
                                      precision)
        }
        for choice in instance.choices
    ]
