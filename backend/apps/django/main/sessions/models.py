from django.db import models
from django_common_utils.libraries.models.mixins import RandomIDMixin
from user_sessions.models import Session

__all__ = [
    "SessionRelation"
]


class SessionRelation(RandomIDMixin):
    session = models.OneToOneField(
        Session,
        on_delete=models.CASCADE,
    )
