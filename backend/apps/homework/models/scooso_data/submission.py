from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils import ScoosoDataMixin
from ...public import *

__all__ = [
    "SubmissionScoosoData"
]


class SubmissionScoosoData(ScoosoDataMixin):
    class Meta:
        verbose_name = _("Einreichung-Scooso-Daten")
        verbose_name_plural = _("Einreichung-Scooso-Daten")
        ordering = ("submission", "scooso_id")
    
    submission = models.ForeignKey(
        SUBMISSION,
        verbose_name=submission_single,
        on_delete=models.CASCADE
    )
