from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin

from apps.django.authentication.user.public import *
from apps.django.authentication.user.public import model_names as auth_names
from apps.django.main.course.public import *
from apps.django.main.course.public import model_names as course_names
from apps.django.main.timetable.mixins import LessonMixin
from apps.django.main.timetable.public import *
from apps.django.main.timetable.public import model_names as timetable_names
from apps.utils.texts import max_length_from_choices
from ..options import ModificationTypeOptions
from ..public import model_names
from ..querysets import ModificationQuerySet

if TYPE_CHECKING:
    from apps.django.authentication.user.models import Teacher
    from apps.django.main.course.models import Room, Subject
    from apps.django.main.timetable.models import Lesson

__all__ = [
    "Modification"
]


class Modification(RandomIDMixin, LessonMixin):
    class Meta:
        verbose_name = model_names.MODIFICATION
        verbose_name_plural = model_names.MODIFICATION_PLURAL
        ordering = ("lesson_date", "lesson__start_hour",)
    
    objects = ModificationQuerySet.as_manager()
    
    lesson = models.ForeignKey(
        LESSON,
        on_delete=models.CASCADE,
        verbose_name=timetable_names.LESSON
    )  # type: Lesson
    
    new_room = models.ForeignKey(
        ROOM,
        on_delete=models.SET_NULL,
        verbose_name=course_names.ROOM,
        blank=True,
        null=True,
    )  # type: Room
    
    new_subject = models.ForeignKey(
        SUBJECT,
        on_delete=models.SET_NULL,
        verbose_name=course_names.SUBJECT,
        blank=True,
        null=True,
    )  # type: Subject
    
    new_teacher = models.ForeignKey(
        TEACHER,
        on_delete=models.SET_NULL,
        verbose_name=auth_names.TEACHER,
        blank=True,
        null=True,
    )  # type: Teacher
    
    information = models.TextField(
        verbose_name=_("Information"),
        blank=True,
        null=True,
        max_length=1023,
    )  # type: str
    
    modification_type = models.CharField(
        choices=ModificationTypeOptions.choices,
        verbose_name=_("Typ"),
        help_text=_("Art von Veränderung"),
        default=ModificationTypeOptions.REPLACEMENT.value,
        max_length=max_length_from_choices(ModificationTypeOptions.choices),
    )  # type: int
