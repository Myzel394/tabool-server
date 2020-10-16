from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = [
    "UserInformationHistoricalModel"
]


class UserInformationHistoricalModel(models.Model):
    class Meta:
        abstract = True
    
    ip_address = models.GenericIPAddressField(
        verbose_name=_("IP-Adresse"),
        blank=True,
        null=True,
    )
