from datetime import datetime
from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_lifecycle import AFTER_CREATE, BEFORE_SAVE, hook, LifecycleModel

from apps.django.main.lesson.public import *
from apps.django.main.lesson.public import model_names as lesson_names
from apps.django.main.school_data.public import *
from apps.django.main.school_data.public import model_names as school_names
from constants import maxlength
from ..notifications import push_modification_change
from ..options import ModificationTypeOptions
from ..public import model_names
from ..querysets import ModificationQuerySet

if TYPE_CHECKING:
    from apps.django.main.school_data.models import Room, Subject, Teacher
    from apps.django.main.lesson.models import Lesson

__all__ = [
    "Modification"
]


class Modification(RandomIDMixin, LifecycleModel):
    class Meta:
        verbose_name = model_names.MODIFICATION
        verbose_name_plural = model_names.MODIFICATION_PLURAL
        ordering = ("lesson__date", "start_datetime",)
    
    objects = ModificationQuerySet.as_manager()
    
    lesson = models.ForeignKey(
        LESSON,
        on_delete=models.CASCADE,
        verbose_name=lesson_names.LESSON
    )  # type: Lesson
    
    new_room = models.ForeignKey(
        ROOM,
        on_delete=models.SET_NULL,
        verbose_name=school_names.ROOM,
        blank=True,
        null=True,
    )  # type: Room
    
    new_subject = models.ForeignKey(
        SUBJECT,
        on_delete=models.SET_NULL,
        verbose_name=school_names.SUBJECT,
        blank=True,
        null=True,
    )  # type: Subject
    
    new_teacher = models.ForeignKey(
        TEACHER,
        on_delete=models.SET_NULL,
        verbose_name=school_names.TEACHER,
        blank=True,
        null=True,
    )  # type: Teacher
    
    information = models.TextField(
        verbose_name=_("Information"),
        blank=True,
        null=True,
        max_length=maxlength.INFORMATION,
    )  # type: str
    
    modification_type = models.PositiveSmallIntegerField(
        choices=ModificationTypeOptions.choices,
        verbose_name=_("Typ"),
        help_text=_("Art von Veränderung"),
        default=ModificationTypeOptions.REPLACEMENT.value
    )  # type: int
    
    start_datetime = models.DateTimeField(
        verbose_name=_("Startzeit"),
        blank=True,
    )
    
    end_datetime = models.DateTimeField(
        verbose_name=_("Endzeit"),
        blank=True,
    )
    
    from_scooso = models.BooleanField(
        default=False,
        verbose_name=_("Von Scooso"),
    )
    
    def __str__(self):
        return str(self.lesson)
    
    @hook(BEFORE_SAVE)
    def _hook_autofill_times(self):
        self.start_datetime = self.start_datetime or datetime.combine(self.lesson.date, self.lesson.start_time)
        self.end_datetime = self.end_datetime or datetime.combine(self.lesson.date, self.lesson.end_time)
    
    @hook(AFTER_CREATE)
    def _hook_send_modification_changed_event(self):
        push_modification_change(self)
