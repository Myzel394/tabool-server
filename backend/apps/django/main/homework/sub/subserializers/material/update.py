from typing import *

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from .base import BaseMaterialSerializer

if TYPE_CHECKING:
    from ....models import Material

__all__ = [
    "UpdateMaterialSerializer"
]


class UpdateMaterialSerializer(BaseMaterialSerializer):
    instance: "Material"
    
    class Meta(BaseMaterialSerializer.Meta):
        fields = [
            "publish_datetime", "announce",
        ]
    
    def validate_announce(self, value: bool):
        if self.instance.announce and not value:
            raise ValidationError(
                _("Sobald das Material einmal angekündigt wurde, kann die Ankündigung nicht mehr verändert werden.")
            )
