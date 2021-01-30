from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers.mixins import TextOptimizerHandler
from django_common_utils.libraries.handlers.models import HandlerMixin
from django_common_utils.libraries.models.mixins import RandomIDMixin

from apps.django.utils.models import AssociatedUserMixin
from ..public import LESSON
from ..public.model_names import LESSON_ABSENCE, LESSON_ABSENCE_PLURAL
from ..querysets import LessonAbsenceQuerySet

__all__ = [
    "LessonAbsence"
]


class LessonAbsence(RandomIDMixin, AssociatedUserMixin, HandlerMixin):
    class Meta:
        verbose_name = LESSON_ABSENCE
        verbose_name_plural = LESSON_ABSENCE_PLURAL
        ordering = ("lesson__date", "lesson__start_time")
        unique_together = (
            ("lesson", "associated_user"),
        )
    
    objects = LessonAbsenceQuerySet.as_manager()
    
    lesson = models.ForeignKey(
        LESSON,
        on_delete=models.CASCADE,
        verbose_name=LESSON
    )
    
    reason = models.CharField(
        max_length=63,
        verbose_name=_("Grund"),
        blank=True,
        null=True,
    )
    
    is_signed = models.BooleanField(
        default=False,
        verbose_name=_("Ist unterschrieben?")
    )
    
    @staticmethod
    def handlers():
        return {
            "reason": TextOptimizerHandler(),
        }
