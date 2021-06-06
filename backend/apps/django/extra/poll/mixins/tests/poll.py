import random

from django.test import TestCase
from django_hint import QueryType

from apps.django.authentication.user.models import User
from apps.django.utils.tests_mixins import joinkwargs
from ...models import Choice, Poll

__all__ = [
    "PollTestMixin"
]


def random_color():
    return "#" + "".join(random.choice("0123456789ABCDEF") for _ in range(6))


class PollTestMixin(TestCase):
    @staticmethod
    def Create_poll(
            choices: list[str] = None,
            targeted_user: QueryType[User] = None,
            **kwargs,
    ) -> Poll:
        choices = choices or ["Ja", "Nein"]
        targeted_user = targeted_user or list(User.objects.all())

        poll = Poll.objects.create(
            **joinkwargs(
                {
                    "title": lambda: "Random title",
                },
                kwargs
            )
        )
        poll.targeted_user.add(*targeted_user)

        for choice_text in choices:
            Choice.objects.create(
                poll=poll,
                text=choice_text,
                color=random_color()
            )

        return poll
