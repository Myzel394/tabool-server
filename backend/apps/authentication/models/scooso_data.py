from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from fernet_fields import EncryptedCharField

from ..querysets import ScoosoDataQuerySet

__all__ = [
    "ScoosoData"
]


class ScoosoData(RandomIDMixin):
    class Meta:
        verbose_name = _("Scooso-Daten")
        verbose_name_plural = _("Scooso-Daten")
        ordering = ("user",)
    
    objects = ScoosoDataQuerySet()
    
    user = models.OneToOneField(
        "authentication.User",
        on_delete=models.CASCADE,
    )
    
    username = EncryptedCharField(
        max_length=127,
        verbose_name=_("Benutzername")
    )
    
    password = EncryptedCharField(
        max_length=127,
        verbose_name=_("Passwort")
    )
