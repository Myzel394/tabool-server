from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers.mixins import TextOptimizerHandler
from django_common_utils.libraries.handlers.models import HandlerMixin
from django_common_utils.libraries.models.mixins import CreationDateMixin, RandomIDMixin
from django_lifecycle import AFTER_CREATE, BEFORE_CREATE, BEFORE_UPDATE, hook

from apps.django.authentication.user.public import *
from apps.django.authentication.user.public import model_names as auth_names
from ..notifications import push_homework_added
from ..public import model_names
from ..querysets import HomeworkQuerySet
from ..validators import validate_private_to_student
from ...timetable.mixins import LessonMixin

if TYPE_CHECKING:
    from datetime import date
    from apps.django.authentication.user.models import User

__all__ = [
    "Homework"
]


class Homework(RandomIDMixin, CreationDateMixin, HandlerMixin, LessonMixin):
    class Meta:
        verbose_name = model_names.HOMEWORK
        verbose_name_plural = model_names.HOMEWORK_PLURAL
        ordering = ("-due_date", "-lesson_date")
        permissions = (
            ("can_view_private_homework", _("Kann private Hausaufgaben sehen und bearbeiten")),
        )
    
    objects = HomeworkQuerySet.as_manager()
    
    private_to_student = models.ForeignKey(
        STUDENT,
        on_delete=models.CASCADE,
        verbose_name=auth_names.STUDENT,
        blank=True,
        null=True,
    )  # type: User
    
    due_date = models.DateTimeField(
        verbose_name=_("Fälligkeitsdatum"),
        blank=True,
        null=True,
    )  # type: date
    
    information = models.TextField(
        verbose_name=_("Informationen"),
        blank=True,
        null=True,
        max_length=1023,
    )  # type: str
    
    type = models.CharField(
        max_length=127,
        verbose_name=_("Hausaufgaben-Typ"),
        help_text=_("Beispiel: Vortag, Hausaufgabe, Protokoll, Hausarbeit"),
        blank=True,
        null=True
    )  # type: str
    
    def clean(self):
        validate_private_to_student(self)
        
        return super().clean()
    
    @property
    def is_private(self) -> bool:
        return self.private_to_student is not None
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="due_date", has_changed=True)
    def _hook_full_clean(self):
        self.full_clean()
    
    @hook(AFTER_CREATE)
    def _hook_send_event(self):
        if not self.is_private:
            push_homework_added(self)
    
    @staticmethod
    def handlers():
        return {
            "information": TextOptimizerHandler()
        }
