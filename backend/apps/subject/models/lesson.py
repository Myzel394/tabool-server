from django.db import models
from django_common_utils.libraries.models import RandomIDMixin
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.utils import model_verbose
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook

from .. import constants, model_references, model_verbose_functions
from ..validators import validate_lesson_weekday
from ..querysets import LessonQuerySet


__all__ = [
    "Lesson"
]


class Lesson(RandomIDMixin):
    class Meta:
        verbose_name = _("Stunde")
        verbose_name_plural = _("Stunden")
        unique_together = (
            ("lesson", "date")
        )
    
    objects = LessonQuerySet.as_manager()
    
    lesson_data = models.ForeignKey(
        model_references.LESSON_DATA,
        verbose_name=model_verbose_functions.lesson_data_single,
        on_delete=models.CASCADE,
    )
    
    date = models.DateField(
        verbose_name=_("Datum")
    )
    
    attendance = models.BooleanField(
        default=True,
        verbose_name=_("Anwesend"),
        help_text=_("Bist du in dieser Stunde anwesend?")
    )
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="date")
    def _hook_validate_date(self):
        validate_lesson_weekday(self.date, self.lesson_data)
