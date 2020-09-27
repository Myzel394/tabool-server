from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models import RandomIDMixin

from apps.utils import UserModelRelationMixin
from ...public import *

if TYPE_CHECKING:
    from .. import Lesson

__all__ = [
    "UserLessonRelation"
]


class UserLessonRelation(RandomIDMixin, UserModelRelationMixin):
    class Meta:
        verbose_name = _("Benutzer-Stunde-Beziehung")
        verbose_name_plural = _("Benutzer-Stunden-Beziehungen")
        unique_together = (
            ("lesson", "user")
        )
        ordering = ("lesson", "user")
    
    lesson = models.ForeignKey(
        LESSON,
        verbose_name=lesson_single,
        on_delete=models.CASCADE
    )  # type: Lesson
    
    attendance = models.BooleanField(
        default=True,
        verbose_name=_("Anwesend?"),
        help_text=_("Bist du in dieser Stunde anwesend?")
    )  # type: bool
