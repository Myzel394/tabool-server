from django.utils.translation import gettext_lazy as _

from .mixins.homework import BaseHomeworkMixin
from ..querysets import TeacherHomeworkQuerySet

__all__ = [
    "TeacherHomework"
]


class TeacherHomework(BaseHomeworkMixin):
    class Meta:
        verbose_name = _("Lehrer-Hausaufgabe")
        verbose_name_plural = _("Lehrer-Hausaufgaben")
        ordering = ("-completed", "due_date")
    
    objects = TeacherHomeworkQuerySet.as_manager()
