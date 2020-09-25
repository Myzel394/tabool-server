from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers import TextOptimizerHandler
from django_common_utils.libraries.models import RandomIDMixin
from django_common_utils.libraries.models.mixins.date import EditCreationDateMixin
from django_common_utils.libraries.utils import model_verbose
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook

from apps.authentication.public import model_references as user_model_references, model_verbose_functions as \
    user_model_verbose_function
from apps.lesson.public import model_references, model_verbose_functions
from ..querysets import HomeworkQuerySet
from ..validators import validate_only_future_days
from ...utils.models import AddedAtMixin
from ...utils.time import format_datetime
from ...utils.validators import validate_weekday_in_lesson_data_available


__all__ = [
    "Homework"
]


class Homework(RandomIDMixin, AddedAtMixin):
    class Meta:
        verbose_name = _("Eigene Hausaufgabe")
        verbose_name_plural = _("Eigene Hausaufgaben")
        ordering = ("-completed", "due_date")
    
    objects = HomeworkQuerySet.as_manager()

    lesson = models.ForeignKey(
        model_references.LESSON,
        on_delete=models.CASCADE,
        verbose_name=model_verbose_functions.lesson_single,
    )
    
    private_to_user = models.ForeignKey(
        user_model_references.USER,
        verbose_name=user_model_verbose_function.user_single,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    due_date = models.DateField(
        verbose_name=_("Fälligkeitsdatum"),
        blank=True,
        null=True
    )

    information = models.TextField(
        verbose_name=_("Informationen"),
        blank=True,
        null=True,
    )

    completed = models.BooleanField(
        verbose_name=_("Erledigt"),
        default=False,
    )
    
    type = models.CharField(
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
        validate_weekday_in_lesson_data_available(self.due_date)

    @staticmethod
    def handlers():
        return {
            "information": TextOptimizerHandler()
        }

    def __str__(self):
        if self.due_date:
            return f"{model_verbose(self.__class__)}: {self.lesson} bis {format_datetime(self.due_date)}"
        return f"{model_verbose(self.__class__)}: {self.lesson}"
    
    @property
    def is_private(self) -> bool:
        return self.private_to_user is not None
