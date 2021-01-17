from typing import *

from django.db import models
from django_common_utils.libraries.models.mixins import CreationDateMixin, RandomIDMixin

from apps.django.utils.models import AssociatedUserMixin
from ..public import model_references
from ..public.model_names import CHOICE_NAME_PLURAL, POLL_NAME, VOTE, VOTE_PLURAL

if TYPE_CHECKING:
    from .poll import *

__all__ = [
    "Vote"
]


class Vote(RandomIDMixin, CreationDateMixin, AssociatedUserMixin):
    class Meta:
        verbose_name = VOTE
        verbose_name_plural = VOTE_PLURAL
    
    poll = models.ForeignKey(
        model_references.POLL,
        verbose_name=POLL_NAME,
        on_delete=models.CASCADE,
    )  # type: Poll
    
    choices = models.ManyToManyField(
        model_references.CHOICE,
        verbose_name=CHOICE_NAME_PLURAL
    )
