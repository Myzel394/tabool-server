from datetime import date
from typing import *

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from .models import LessonData

__all__ = [
    "validate_lesson_weekday"
]


def validate_lesson_weekday(actual_date: date, lesson: "LessonData"):
    if (weekday := actual_date.weekday()) != lesson.weekday:
        raise ValidationError(_(
            "Der Wochentag für diese Schulstunde ist nicht gültig"
        ).format(weekday=weekday, lesson_weekday=lesson.weekday))
