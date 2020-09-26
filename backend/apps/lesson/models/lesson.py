from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models import RandomIDMixin
from django_hint import QueryType
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook

from .user_relations.lesson import UserLessonRelation
from ..public import model_references, model_verbose_functions
from ..querysets import LessonQuerySet
from ..validators import validate_lesson_weekday
from ...utils.models import RelationMixin

if TYPE_CHECKING:
    from datetime import date as typing_date
    from . import LessonData
    from apps.homework.models import Homework

__all__ = [
    "Lesson"
]


class Lesson(RandomIDMixin, RelationMixin):
    class Meta:
        verbose_name = _("Stunde")
        verbose_name_plural = _("Stunden")
        unique_together = (
            ("lesson_data", "date")
        )
    
    get_relation: UserLessonRelation
    RELATED_MODEL = UserLessonRelation
    
    objects = LessonQuerySet.as_manager()
    
    lesson_data = models.ForeignKey(
        model_references.LESSON_DATA,
        verbose_name=model_verbose_functions.lesson_data_single,
        on_delete=models.CASCADE,
    )  # type: LessonData
    
    date = models.DateField(
        verbose_name=_("Datum")
    )  # type: typing_date
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="date")
    def _hook_validate_date(self):
        validate_lesson_weekday(self.date, self.lesson_data)
    
    @property
    def homeworks(self) -> QueryType["Homework"]:
        return self.homework_set.all()
