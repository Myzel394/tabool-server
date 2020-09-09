from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers.mixins import TextOptimizerHandler
from django_common_utils.libraries.models import HandlerMixin, RandomIDMixin
from django_common_utils.libraries.utils import model_verbose
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from apps.homework.validators import validate_only_future_dates
from apps.timetable.models import Subject
from apps.utils.models import AssociatedUserMixin
from constants import maxlength

__all__ = [
    "Homework"
]


class Homework(RandomIDMixin, HandlerMixin, LifecycleModel):
    class Meta:
        verbose_name = _("Hausaufgabe")
        verbose_name_plural = _("Hausaufgaben")
    
    due_date = models.DateField(
        verbose_name=_("Fälligkeitsdatum"),
        blank=True,
        null=True
    )
    
    subject = models.ForeignKey(
        Subject,
        verbose_name=model_verbose(Subject),
        on_delete=models.CASCADE
    )
    
    title = models.CharField(
        verbose_name=_("Überschrift"),
        max_length=maxlength.HOMEWORK,
        blank=True,
        null=True,
    )
    
    description = models.TextField(
        verbose_name=_("Beschreibung"),
        blank=True,
        null=True,
    )
    
    def __str__(self):
        return f"{self.subject}: {self.subject[:10]}..."
    
    @staticmethod
    def handlers():
        return {
            "description": TextOptimizerHandler()
        }
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="due_date")
    def _hook_due_date_validation(self):
        validate_only_future_dates(self.due_date)


"""
class Submission(RandomIDMixin, AssociatedUserMixin, DatesMixin):
    class Meta:
        verbose_name = _("Einreichung")
        verbose_name_plural = _("Einreichungen")
        ordering = ("-last_edited_at", "-created_at")
    
    homework = models.ForeignKey(
        Homework,
        verbose_name=model_verbose(Homework),
        on_delete=models.CASCADE,
    )
    
    files = models.ManyToManyField(
        "SubmissionFile",
        verbose_name=model_verbose_plural("SubmissionFile"),
    )


class SubmissionFile(RandomIDMixin, AssociatedUserMixin, DatesMixin):
    class Meta:
        verbose_name = _("Datei-Einreichung")
        verbose_name_plural = _("Datei-Einreichungen")
        ordering = ("-last_edited_at", "-created_at")
    
    file = models.FileField(
        verbose_name=_("Datei"),
    )
    
    name = models.CharField(
        verbose_name=_("Dateienname")
    )"""
