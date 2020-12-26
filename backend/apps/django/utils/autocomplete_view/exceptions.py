from dataclasses import dataclass

from django.utils.translation import gettext_lazy as _


@dataclass
class InvalidQueryError(Exception):
    message: str = _("Ungültige Eingabe")
