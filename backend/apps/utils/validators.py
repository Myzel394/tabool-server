import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_place(value: str) -> None:
    if not re.match("^(([A-Z]*[0-9]+)|([a-zA-Z]+))$", value):
        raise ValidationError(
            _('Der Raum "{}" ist nicht gültig.').format(value)
        )
