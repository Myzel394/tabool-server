from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.django.utils.models import ScoosoDataMixin
from ...public import *
from ...public import model_verboses

if TYPE_CHECKING:
    from .. import Teacher

__all__ = [
    "TeacherScoosoData"
]


class TeacherScoosoData(ScoosoDataMixin):
    class Meta:
        verbose_name = model_verboses.TEACHER_SCOOSO
        verbose_name_plural = model_verboses.TEACHER_SCOOSO_PLURAL
        ordering = ("code", "scooso_id")
    
    teacher = models.OneToOneField(
        TEACHER,
        on_delete=models.CASCADE,
        verbose_name=model_verboses.TEACHER
    )  # type: Teacher
    
    code = models.CharField(
        max_length=127,
        verbose_name=_("Lehrer-Code"),
        blank=True,
        null=True
    )  # type: str
    
    def __str__(self):
        return str(self.teacher)
