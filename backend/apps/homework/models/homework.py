from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers import TextOptimizerHandler
from django_common_utils.libraries.models import RandomIDMixin
from django_common_utils.libraries.models.mixins.date import CreationDateMixin
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook
from simple_history.models import HistoricalRecords

from apps.authentication.public import *
from apps.history_extras.extras import UserInformationHistoricalModel
from apps.lesson.public import *
from apps.utils import format_datetime, RelationMixin, validate_weekday_in_lesson_data_available
from .user_relations.homework import UserHomeworkRelation
from ..querysets import HomeworkQuerySet
from ..validators import validate_only_future_days

if TYPE_CHECKING:
    from datetime import date, datetime
    from apps.lesson.models import Lesson
    from django.contrib.auth import get_user_model

__all__ = [
    "Homework"
]


class Homework(RandomIDMixin, CreationDateMixin, RelationMixin):
    class Meta:
        verbose_name = _("Hausaufgabe")
        verbose_name_plural = _("Hausaufgaben")
        ordering = ("due_date", "type")
    
    get_relation: UserHomeworkRelation
    RELATED_MODEL = UserHomeworkRelation
    
    objects = HomeworkQuerySet.as_manager()
    
    lesson = models.ForeignKey(
        LESSON,
        on_delete=models.CASCADE,
        verbose_name=lesson_single,
    )  # type: Lesson
    
    private_to_user = models.ForeignKey(
        USER,
        verbose_name=user_single,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )  # type: get_user_model()
    
    due_date = models.DateField(
        verbose_name=_("Fälligkeitsdatum"),
        blank=True,
        null=True
    )  # type: date
    
    information = models.TextField(
        verbose_name=_("Informationen"),
        blank=True,
        null=True,
    )  # type: str
    
    type = models.CharField(
        max_length=127,
        verbose_name=_("Hausaufgaben-Typ"),
        help_text=_("Beispiel: Vortag, Hausaufgabe, Protokoll, Hausarbeit"),
        blank=True,
        null=True
    )  # type: str
    
    history = HistoricalRecords(
        cascade_delete_history=True,
        excluded_fields=["private_to_user", "creation_date"],
        bases=[UserInformationHistoricalModel]
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
    
    @property
    def edited_at(self) -> "datetime":
        return self.history.all().latest().history_date
