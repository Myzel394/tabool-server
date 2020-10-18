from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers.mixins import TextOptimizerHandler
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_common_utils.libraries.models.mixins.date import CreationDateMixin
from django_eventstream import send_event
from django_hint import QueryType
from django_lifecycle import AFTER_CREATE, BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel
from simple_history.models import HistoricalRecords

from apps.django.main.authentication.public import *
from apps.django.main.authentication.public import model_names as auth_names
from apps.django.main.lesson.public import *
from apps.django.main.lesson.public import model_names as lesson_names
from apps.django.utils.history_extras.extras import UserInformationHistoricalModel
from apps.django.utils.validators import validate_weekday_in_lesson_data_available
from .user_relations.homework import UserHomeworkRelation
from ..public import HOMEWORK_CHANNEL, model_names
from ..querysets import HomeworkQuerySet
from ..validators import validate_only_future_days

if TYPE_CHECKING:
    from datetime import date, datetime
    from . import UserHomeworkRelation
    from apps.django.main.lesson.models import Lesson
    from apps.django.main.authentication.models import User

__all__ = [
    "Homework"
]


class Homework(RandomIDMixin, CreationDateMixin, LifecycleModel):
    class Meta:
        verbose_name = model_names.HOMEWORK
        verbose_name_plural = model_names.HOMEWORK_PLURAL
        ordering = ("due_date", "type")
    
    objects = HomeworkQuerySet.as_manager()
    
    lesson = models.ForeignKey(
        LESSON,
        on_delete=models.CASCADE,
        verbose_name=lesson_names.LESSON,
    )  # type: Lesson
    
    private_to_user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        verbose_name=auth_names.USER,
        blank=True,
        null=True,
    )  # type: User
    
    due_date = models.DateField(
        verbose_name=_("Fälligkeitsdatum"),
        blank=True,
        null=True,
        validators=[validate_only_future_days, validate_weekday_in_lesson_data_available]
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
        excluded_fields=["private_to_user", "created_at"],
        bases=[UserInformationHistoricalModel]
    )
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="due_date", has_changed=True)
    def _hook_full_clean(self):
        self.full_clean()
    
    @hook(AFTER_CREATE)
    def _hook_send_event(self):
        if not self.is_private:
            send_event(HOMEWORK_CHANNEL, "homework", {
                "lesson_id": self.lesson_id
            })
    
    @staticmethod
    def handlers():
        return {
            "information": TextOptimizerHandler()
        }
    
    def __str__(self):
        if self.due_date:
            return _("{lesson} (Typ: {type}) bis {due_date} (Privat: {is_private}").format(
                lesson=self.lesson,
                type=self.type,
                due_date=self.due_date,
                is_private=self.private_to_user is not None
            )
        return _("{lesson} (Typ: {type}, Privat: {is_private})").format(
            lesson=self.lesson,
            type=self.type,
            is_private=self.private_to_user is not None
        )
    
    @property
    def is_private(self) -> bool:
        return self.private_to_user is not None
    
    @property
    def edited_at(self) -> "datetime":
        return self.history.latest().history_date
    
    @property
    def user_relations(self) -> QueryType["UserHomeworkRelation"]:
        return self.userhomeworkrelation_set.all()