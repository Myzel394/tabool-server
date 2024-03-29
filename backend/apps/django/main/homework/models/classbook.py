from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers.mixins import TextOptimizerHandler
from django_common_utils.libraries.handlers.models import HandlerMixin
from django_common_utils.libraries.models.mixins import RandomIDMixin

from apps.django.main.timetable.mixins import LessonMixin
from ..public import model_names
from ..querysets import ClassbookQuerySet

__all__ = [
    "Classbook"
]


class Classbook(RandomIDMixin, LessonMixin, HandlerMixin):
    class Meta:
        verbose_name = model_names.CLASSBOOK
        verbose_name_plural = model_names.CLASSBOOK_PLURAL
        ordering = ("lesson_date",)
        unique_together = (
            ("lesson", "lesson_date")
        )

    objects = ClassbookQuerySet.as_manager()

    presence_content = models.TextField(
        verbose_name=_("Inhalt Präsenzunterricht"),
        blank=True,
        null=True,
    )
    online_content = models.TextField(
        verbose_name=_("Inhalt Fernunterricht"),
        blank=True,
        null=True,
    )

    video_conference_link = models.URLField(
        max_length=1023,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.lesson)

    @staticmethod
    def handlers():
        return {
            "presence_content": TextOptimizerHandler(),
            "online_content": TextOptimizerHandler()
        }
