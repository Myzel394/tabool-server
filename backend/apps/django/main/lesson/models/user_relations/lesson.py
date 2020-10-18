from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin

from apps.django.utils.models import UserModelRelationMixin
from ...public import *
from ...public import model_names

if TYPE_CHECKING:
    from .. import Lesson

__all__ = [
    "UserLessonRelation"
]


class UserLessonRelation(RandomIDMixin, UserModelRelationMixin):
    class Meta:
        verbose_name = model_names.LESSON_RELATION
        verbose_name_plural = model_names.LESSON_RELATION_PLURAL
        unique_together = (
            ("lesson", "user")
        )
        ordering = ("lesson", "user")
    
    lesson = models.ForeignKey(
        LESSON,
        on_delete=models.CASCADE,
        verbose_name=model_names.LESSON
    )  # type: Lesson
    
    attendance = models.BooleanField(
        default=True,
        verbose_name=_("Anwesend?"),
        help_text=_("Bist du in dieser Stunde anwesend?")
    )  # type: bool
    
    def __str__(self):
        return str(self.lesson)
