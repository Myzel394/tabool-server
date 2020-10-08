from django.db import models
from django_common_utils.libraries.models import RandomIDMixin
from django.utils.translation import gettext_lazy as _

from apps.utils import ScoosoDataMixin
from ...public import *

__all__ = [
    "MaterialScoosoData"
]


class MaterialScoosoData(RandomIDMixin, ScoosoDataMixin):
    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materialien")
        ordering = ("material", "scooso_id")
    
    material = models.OneToOneField(
        MATERIAL,
        verbose_name=material_single,
        on_delete=models.CASCADE,
    )
    
    owner_id = models.PositiveSmallIntegerField(
        verbose_name=_("Besitzer-Scooso-ID"),
        blank=True,
        null=True
    )
