from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_eventstream import send_event
from django_lifecycle import AFTER_CREATE, AFTER_DELETE, AFTER_UPDATE, hook, LifecycleModel

from apps.django.main.lesson.public import *
from apps.django.main.lesson.public import model_names as lesson_names
from apps.django.main.school_data.public import *
from apps.django.main.school_data.public import model_names as school_names
from ..options import ModificationTypeOptions
from ..public import model_names, MODIFICATION_CHANNEL
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
        ordering = ("lesson",)
    
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
        null=True
    )  # type: str
    
    modification_type = models.PositiveSmallIntegerField(
        choices=ModificationTypeOptions.choices,
        verbose_name=_("Typ"),
        help_text=_("Art von Veränderung"),
        default=ModificationTypeOptions.REPLACEMENT.value
    )  # type: int
    
    def __str__(self):
        return str(self.lesson)
    
    @hook(AFTER_CREATE)
    @hook(AFTER_DELETE)
    @hook(
        AFTER_UPDATE,
        when_any=["new_room", "new_teacher", "new_subject", "information", "modification_type"]
    )
    def _hook_send_modification_changed_event(self):
        send_event(MODIFICATION_CHANNEL, "modification", {
            "lesson_id": self.lesson_id
        })
