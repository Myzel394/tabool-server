from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_hint import QueryType
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook

from apps.utils import format_datetime
from .user_relations.lesson import UserLessonRelation
from ..public import *
from ..public import model_names
from ..querysets import LessonQuerySet
from ..validators import validate_lesson_weekday

if TYPE_CHECKING:
    from datetime import date as typing_date
    from . import LessonData, UserLessonRelation
    from apps.django.main.homework.models import Homework

__all__ = [
    "Lesson"
]


class Lesson(RandomIDMixin):
    class Meta:
        verbose_name = model_names.LESSON
        verbose_name_plural = model_names.LESSON_PLURAL
        unique_together = (
            ("lesson_data", "date")
        )
        ordering = ("date", "lesson_data")
    
    objects = LessonQuerySet.as_manager()
    
    lesson_data = models.ForeignKey(
        LESSON_DATA,
        on_delete=models.CASCADE,
        verbose_name=model_names.LESSON_DATA
    )  # type: LessonData
    
    date = models.DateField(
        verbose_name=_("Datum")
    )  # type: typing_date
    
    def __str__(self):
        return _("{date}, {course}").format(
            date=format_datetime(self.date),
            course=self.lesson_data.course
        )
    
    def clean(self):
        validate_lesson_weekday(self.date, self.lesson_data)
        return super().clean()
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when_any=["date", "lesson_data"], has_changed=True)
    def _hook_full_clean(self):
        self.full_clean()
    
    @property
    def homeworks(self) -> QueryType["Homework"]:
        return self.homework_set.all()
    
    @property
    def user_relations(self) -> QueryType["UserLessonRelation"]:
        return self.userlessonrelation_set.all()
