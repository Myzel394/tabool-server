import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

__all__ = [
    "validate_place"
]


def validate_place(value: str) -> None:
    if not re.match("^(([A-Z]{1,2}[0-9]?)|([0-9]){3})|([A-Z][A-z ]{62})$", value):
        raise ValidationError(
            _("Dieser Raum ist nicht gültig.")
        )
