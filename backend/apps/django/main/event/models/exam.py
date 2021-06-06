from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import CreationDateMixin, RandomIDMixin

from apps.django.main.course.public import *
from apps.django.main.course.public import model_names as course_names
from ..public import model_names
from ..querysets import ExamQuerySet

if TYPE_CHECKING:
    from apps.django.main.course.models import Course

__all__ = [
    "Exam"
]


class Exam(RandomIDMixin, CreationDateMixin):
    class Meta:
        verbose_name = model_names.EXAM
        verbose_name_plural = model_names.EXAM_PLURAL
        ordering = ("title", "date")

    objects = ExamQuerySet.as_manager()

    course = models.ForeignKey(
        COURSE,
        on_delete=models.CASCADE,
        verbose_name=course_names.COURSE,
    )  # type: Course

    date = models.DateField(
        verbose_name=_("Datum"),
        help_text=_("Datum, wann die Klassenarbeit geschrieben wird."),
    )

    title = models.CharField(
        verbose_name=_("Titel"),
        max_length=31,
    )

    information = models.TextField(
        verbose_name=_("Informationen"),
        max_length=1023,
    )
