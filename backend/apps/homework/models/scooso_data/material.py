from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.scooso_scraper import constants as scraper_constants
from apps.scooso_scraper.scrapers.material import MaterialRequest
from apps.scooso_scraper.utils import build_url
from apps.utils import ScoosoDataMixin
from ...public import *

if TYPE_CHECKING:
    from apps.authentication.models import User

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
    
    def build_download_url(self, user: "User") -> str:
        # TODO: Find better solution!
        scraper = MaterialRequest(user.scoosodata.username, user.scoosodata.password)
        
        url = build_url(
            scraper_constants.MATERIAL_DOWNLOAD_CONNECTION["url"],
            {
                "cmd": 3000,
                "subcmd": 20,
                "varname": "file",
                **scraper.login_data
            }
        )
        suffix = f"&file[{self.scooso_id}]=on"
        
        return url + suffix
