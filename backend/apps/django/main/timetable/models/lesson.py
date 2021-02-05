from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from apps.django.main.course.public import *
from apps.django.main.course.public import model_names as course_names
from apps.django.utils.fields import WeekdayField
from ..public import *
from ..public import model_names
from ..sub.subquerysets.lesson import LessonQuerySet
from ..validators import validate_no_timetable_overlap

if TYPE_CHECKING:
    from apps.django.main.course.models import Course
    from . import Timetable

__all__ = [
    "Lesson"
]


class Lesson(RandomIDMixin, LifecycleModel):
    class Meta:
        verbose_name = model_names.LESSON
        verbose_name_plural = model_names.LESSON_PLURAL
        ordering = ("weekday", "start_hour", "end_hour")
    
    objects = LessonQuerySet.as_manager()
    
    timetable = models.ForeignKey(
        TIMETABLE,
        on_delete=models.CASCADE,
        verbose_name=model_names.TIMETABLE
    )  # type: Timetable
    
    course = models.ForeignKey(
        COURSE,
        on_delete=models.CASCADE,
        verbose_name=course_names.COURSE
    )  # type: Course
    
    weekday = WeekdayField(
        verbose_name=_("Wochentag")
    )
    
    start_hour = models.PositiveSmallIntegerField(
        verbose_name=_("Anfangsstunde")
    )
    
    end_hour = models.PositiveSmallIntegerField(
        verbose_name=_("Endstunde")
    )
    
    def clean(self):
        validate_no_timetable_overlap(self)
        
        return super().clean()
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="timetable", has_changed=True)
    def _hook_full_clean(self):
        self.full_clean()
