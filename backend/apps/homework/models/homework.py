from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins.date import EditCreationDateMixin

from .mixins.homework import BaseHomeworkMixin
from ..querysets import HomeworkQuerySet

__all__ = [
    "Homework"
]


class Homework(BaseHomeworkMixin, EditCreationDateMixin):
    class Meta:
        verbose_name = _("Eigene Hausaufgabe")
        verbose_name_plural = _("Eigene Hausaufgaben")
        ordering = ("-completed", "due_date")
    
    type = models.CharField(
        max_length=127,
        verbose_name=_("Hausaufgaben-Typ"),
        help_text=_("Beispiel: Vortag, Hausaufgabe, Protokoll, Hausarbeit"),
        blank=True,
        null=True
    )
    
    objects = HomeworkQuerySet.as_manager()
