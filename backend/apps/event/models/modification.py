from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_lifecycle import LifecycleModel

from apps.lesson.public import *
from apps.school_data.public import *
from ..options import ModificationTypeOptions
from ..querysets import ModificationQuerySet

if TYPE_CHECKING:
    from datetime import datetime
    from apps.school_data.models import Room, Subject, Teacher
    from apps.lesson.models import Course

__all__ = [
    "Modification"
]


class Modification(RandomIDMixin, LifecycleModel):
    class Meta:
        verbose_name = _("Veränderung")
        verbose_name_plural = _("Veränderungen")
        ordering = ("start_datetime",)
    
    objects = ModificationQuerySet.as_manager()
    
    course = models.ForeignKey(
        COURSE,
        verbose_name=course_single,
        on_delete=models.CASCADE,
    )  # type: Course
    
    new_room = models.ForeignKey(
        ROOM,
        verbose_name=room_single,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )  # type: Room
    
    new_teacher = models.ForeignKey(
        TEACHER,
        verbose_name=teacher_single,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )  # type: Teacher
    
    new_subject = models.ForeignKey(
        SUBJECT,
        verbose_name=subject_single,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )  # type: Subject
    
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
