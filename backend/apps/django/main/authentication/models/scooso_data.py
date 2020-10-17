from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from fernet_fields import EncryptedCharField

from ..public import model_verboses
from ..querysets import ScoosoDataQuerySet

__all__ = [
    "ScoosoData"
]


class ScoosoData(RandomIDMixin):
    class Meta:
        verbose_name = model_verboses.SCOOSO_DATA
        verbose_name_plural = model_verboses.SCOOSO_DATA_PLURAL
        ordering = ("user",)
    
    objects = ScoosoDataQuerySet()
    
    user = models.OneToOneField(
        "authentication.User",
        on_delete=models.CASCADE,
        verbose_name=model_verboses.USER,
    )
    
    username = EncryptedCharField(
        max_length=127,
        verbose_name=_("Benutzername")
    )
    
    password = EncryptedCharField(
        max_length=127,
        verbose_name=_("Passwort")
    )
    
    def __str__(self):
        return str(self.user)
