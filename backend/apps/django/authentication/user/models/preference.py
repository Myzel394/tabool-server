from typing import *

from django.db import models

from apps.django.utils.models import IdMixin
from ..public import *
from ..public import model_names

if TYPE_CHECKING:
    from . import User

__all__ = [
    "Preference"
]


class Preference(IdMixin):
    class Meta:
        verbose_name = model_names.PREFERENCE
        verbose_name_plural = model_names.PREFERENCE_PLURAL
        ordering = ("user",)
    
    data = models.TextField(
        max_length=16384 - 1,
        default="{}"
    )  # type: str
    
    user = models.OneToOneField(
        USER,
        on_delete=models.CASCADE,
    )  # type: User
