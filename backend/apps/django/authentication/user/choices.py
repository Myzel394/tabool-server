from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = [
    "GenderChoices"
]


class GenderChoices(models.TextChoices):
    MALE = "MALE", _("Männlich")
    FEMALE = "FEMALE", _("Weiblich")
    DIVERSE = "DIVERSE", _("Divers")
