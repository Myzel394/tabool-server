from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils import ScoosoDataMixin
from ...public import *

__all__ = [
    "TeacherScoosoData"
]


class TeacherScoosoData(ScoosoDataMixin):
    class Meta:
        verbose_name = _("Lehrer-Scooso-Daten")
        verbose_name_plural = _("Lehrer-Scooso-Daten")
        ordering = ("code", "scooso_id")
        
    teacher = models.OneToOneField(
        TEACHER,
        verbose_name=teacher_single,
        on_delete=models.CASCADE,
    )
    
    code = models.CharField(
        max_length=127,
        blank=True,
        null=True,
        verbose_name=_("Lehrer-Code")
    )

