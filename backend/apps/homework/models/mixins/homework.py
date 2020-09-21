from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers import HandlerMixin
from django_common_utils.libraries.handlers.mixins import TextOptimizerHandler
from django_common_utils.libraries.models import RandomIDMixin
from django_common_utils.libraries.utils import model_verbose
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from apps.subject.models.lesson import Lesson
from apps.utils.models import AddedAtMixin
from apps.utils.time import format_datetime
from ...validators import validate_only_future_days

__all__ = [
    "BaseHomeworkMixin"
]


class BaseHomeworkMixin(
    RandomIDMixin,
    AddedAtMixin,
    
    HandlerMixin,
    LifecycleModel,
):
    class Meta:
        abstract = True
    
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name=model_verbose(Lesson),
    )
    
    due_date = models.DateTimeField(
        verbose_name=_("Fälligkeitsdatum"),
        blank=True,
        null=True
    )
    
    information = models.TextField(
        verbose_name=_("Informationen"),
    )
    
    completed = models.BooleanField(
        verbose_name=_("Erledigt"),
        default=False,
    )
    
    homework_type = models.CharField(
        max_length=127,
        verbose_name=_("Hausaufgaben-Typ"),
        help_text=_("Beispiel: Vortag, Hausaufgabe, Protokoll, Hausarbeit"),
        blank=True,
        null=True
    )
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="due_date")
    def _hook_due_date_validation(self):
        validate_only_future_days(self.due_date)
    
    @staticmethod
    def handlers():
        return {
            "information": TextOptimizerHandler()
        }
    
    def __str__(self):
        if self.due_date:
            return f"{model_verbose(self.__class__)}: {self.lesson} bis {format_datetime(self.due_date)}"
        return f"{model_verbose(self.__class__)}: {self.lesson}"
