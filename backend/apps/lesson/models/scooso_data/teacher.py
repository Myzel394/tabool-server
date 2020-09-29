from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models import RandomIDMixin

from apps.utils import ScoosoDataMixin
from ...public import *


class TeacherScoosoData(ScoosoDataMixin):
    class Meta:
        verbose_name = _("Lehrer-Scooso-Daten")
        verbose_name_plural = _("Lehrer-Scooso-Daten")
        
    teacher = models.OneToOneField(
        TEACHER,
        verbose_name=teacher_single,
        on_delete=models.CASCADE,
    )

