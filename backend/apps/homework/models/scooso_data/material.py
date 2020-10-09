from django.db import models
from django_common_utils.libraries.models import RandomIDMixin
from django.utils.translation import gettext_lazy as _

from apps.scooso_scraper.utils import build_url
from apps.utils import ScoosoDataMixin
from ...public import *
from apps.scooso_scraper import constants as scraper_constants

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
    
    def build_download_url(self, **kwargs) -> str:
        # TODO: Make build_urls for each connection to one function!
        url = build_url(
            scraper_constants.MATERIAL_DOWNLOAD_CONNECTION["url"],
            {
                "cmd": 3000,
                "subcmd": 20,
                "varname": "file",
                **kwargs
            }
        )
        suffix = f"&file[{self.scooso_id}]=on"
        
        return url + suffix
