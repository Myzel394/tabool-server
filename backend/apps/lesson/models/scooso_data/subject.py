from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.lesson.public import *
from apps.utils import ScoosoDataMixin

__all__ = [
    "SubjectScoosoData"
]


class SubjectScoosoData(ScoosoDataMixin):
    class Meta:
        verbose_name = _("Fach-Scooso-Daten")
        verbose_name_plural = _("Fach-Scooso-Daten")
        ordering = ("code", "scooso_id")
    
    subject = models.OneToOneField(
        SUBJECT,
        verbose_name=subject_single,
        on_delete=models.CASCADE,
    )
    
    code = models.CharField(
        verbose_name=_("Fach-Code"),
        max_length=127,
        blank=True,
        null=True
    )

