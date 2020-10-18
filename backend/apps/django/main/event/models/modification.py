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
    from datetime import datetime
    from apps.django.main.school_data.models import Room, Subject, Teacher
    from apps.django.main.lesson.models import Course

__all__ = [
    "Modification"
]


class Modification(RandomIDMixin, LifecycleModel):
    class Meta:
        verbose_name = model_names.MODIFICATION
        verbose_name_plural = model_names.MODIFICATION_PLURAL
        ordering = ("start_datetime",)
    
    objects = ModificationQuerySet.as_manager()
    
    course = models.ForeignKey(
        COURSE,
        on_delete=models.CASCADE,
        verbose_name=lesson_names.COURSE,
    )  # type: Course
    
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
    
    start_datetime = models.DateTimeField(
        verbose_name=_("Start"),
    )  # type: datetime
    
    end_datetime = models.DateTimeField(
        verbose_name=_("Ende")
    )  # type: datetime
    
    information = models.TextField(
        verbose_name=_("Information"),
        blank=True,
        null=True
    )  # type: str
    
    modification_type = models.PositiveSmallIntegerField(
        choices=ModificationTypeOptions.choices,
        verbose_name=_("Typ"),
        help_text=_("Art von Veränderung")
    )  # type: int
    
    def __str__(self):
        return _("{course} vom {start_datetime} bis {end_datetime}").format(
            course=self.course,
            start_datetime=self.start_datetime,
            end_datetime=self.end_datetime
        )
    
    @hook(AFTER_CREATE)
    @hook(AFTER_DELETE)
    @hook(
        AFTER_UPDATE,
        when_any=["new_room", "new_teacher", "new_subject", "start_datetime", "end_datetime", "information"]
    )
    def _hook_send_modification_changed_event(self):
        send_event(MODIFICATION_CHANNEL, "modification", {
            "course_id": self.course_id
        })
