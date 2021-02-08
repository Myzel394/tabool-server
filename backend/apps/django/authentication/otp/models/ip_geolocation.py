from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.django.utils.models import IdMixin
from ..public import model_names

__all__ = [
    "IPGeolocation"
]


class IPGeolocation(IdMixin):
    class Meta:
        verbose_name = model_names.IP_GEOLOCATION
        verbose_name_plural = model_names.IP_GEOLOCATION_PLURAL
        ordering = ("city", "ip_address")
    
    ip_address = models.GenericIPAddressField(
        verbose_name=_("Ip-Adresse"),
    )
    
    longitude = models.FloatField()
    latitude = models.FloatField()
    
    city = models.CharField(
        verbose_name=_("Stadt"),
        max_length=511,
        blank=True,
        null=True
    )
    
    # pragma: no cover
    @property
    def position(self) -> str:
        return f"{self.longitude} {self.latitude}"
