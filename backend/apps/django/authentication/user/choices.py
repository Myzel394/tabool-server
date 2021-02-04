from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = [
    "GenderChoices"
]


class GenderChoices(models.TextChoices):
    MALE = "MAN", _("Männlich")
    FEMALE = "WOMAN", _("Weiblich")
    DIVERSE = "DIVERSE", _("Divers")
