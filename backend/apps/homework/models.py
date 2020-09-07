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
    
    description = models.CharField(
        max_length=maxlength.HOMEWORK,
        verbose_name=_("Beschreibung")
    )
    
    completed = models.BooleanField(
        default=False,
        verbose_name=_("Erledigt")
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
    
    def complete(self):
        """Marks the homework as completed"""
        self.completed = True
        self.save()
