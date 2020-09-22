from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins.date import EditCreationDateMixin

from .mixins.homework import BaseHomeworkMixin
from ..querysets import UserHomeworkQuerySet

__all__ = [
    "UserHomework"
]


class UserHomework(BaseHomeworkMixin, EditCreationDateMixin):
    class Meta:
        verbose_name = _("Eigene Hausaufgabe")
        verbose_name_plural = _("Eigene Hausaufgaben")
        ordering = ("-completed", "due_date")
    
    homework_type = models.CharField(
        max_length=127,
        verbose_name=_("Hausaufgaben-Typ"),
        help_text=_("Beispiel: Vortag, Hausaufgabe, Protokoll, Hausarbeit"),
        blank=True,
        null=True
    )
    
    objects = UserHomeworkQuerySet.as_manager()
