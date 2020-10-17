from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.django.extra.scooso_scraper.scrapers.material import MaterialRequest
from apps.django.utils.models import ScoosoDataMixin
from ...public import *

if TYPE_CHECKING:
    from apps.django.main.authentication.models import User

__all__ = [
    "MaterialScoosoData"
]


class MaterialScoosoData(ScoosoDataMixin):
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
    
    def __str__(self):
        return str(self.material)
    
    def build_download_url(self, user: "User") -> str:
        with MaterialRequest(user.scoosodata.username, user.scoosodata.password) as scraper:
            url = scraper.build_download_material_url(self.scooso_id)
        
        return url
