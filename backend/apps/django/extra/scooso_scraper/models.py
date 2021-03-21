from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import CreationDateMixin, RandomIDMixin

__all__ = [
    "ScoosoRequest"
]


class ScoosoRequest(RandomIDMixin, CreationDateMixin):
    class Meta:
        verbose_name = _("Scooso-Anfrage")
        verbose_name_plural = _("Scooso-Anfragen")
        ordering = ("created_at",)
    
    EXPIRE_DAYS = 10
    
    response = models.CharField(
        max_length=131_072 - 1,
    )
    
    name = models.CharField(
        max_length=255,
    )
