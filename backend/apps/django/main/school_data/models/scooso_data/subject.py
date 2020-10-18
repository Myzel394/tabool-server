from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.django.utils.models import ScoosoDataMixin
from ...public import *
from ...public import model_names

if TYPE_CHECKING:
    from .. import Subject

__all__ = [
    "SubjectScoosoData"
]


class SubjectScoosoData(ScoosoDataMixin):
    class Meta:
        verbose_name = model_names.SUBJECT_SCOOSO
        verbose_name_plural = model_names.SUBJECT_SCOOSO_PLURAL
        ordering = ("code", "scooso_id")
    
    subject = models.OneToOneField(
        SUBJECT,
        on_delete=models.CASCADE,
        verbose_name=model_names.SUBJECT
    )  # type: Subject
    
    code = models.CharField(
        verbose_name=_("Fach-Code"),
        max_length=127,
        blank=True,
        null=True
    )  # type: str
    
    def __str__(self):
        return str(self.subject)
