from django.db import models
from django.utils.translation import gettext_lazy as _
from fernet_fields import EncryptedCharField

__all__ = [
    "ScoosoData"
]


class ScoosoData(models.Model):
    class Meta:
        verbose_name = _("Scooso-Daten")
        verbose_name_plural = _("Scooso-Daten")
    
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
