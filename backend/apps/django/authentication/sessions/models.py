from django.db import models
from user_sessions.models import Session

from apps.django.utils.models import IdMixin

__all__ = [
    "SessionRelation"
]


class SessionRelation(IdMixin):
    session = models.OneToOneField(
        Session,
        on_delete=models.CASCADE,
    )
