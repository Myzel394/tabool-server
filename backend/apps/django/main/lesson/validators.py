import calendar
from datetime import date
from typing import *

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.utils import format_datetime

if TYPE_CHECKING:
    from .models import Lesson

__all__ = [
    "validate_lesson_weekday"
]


def validate_lesson_weekday(actual_date: date, lesson: "Lesson"):
    abbreviations = list(calendar.day_abbr)
    
    if (weekday := actual_date.weekday()) != lesson.weekday:
        raise ValidationError(_(
            "Der Wochentag für das Datum {date} ist ein {weekday}, der festgelegte Wochentag für die Stunde ist jedoch "
            "{lesson_weekday}. Die Wochentage müssen gleich sein."
        ).format(
            date=format_datetime(actual_date),
            weekday=abbreviations[weekday],
            lesson_weekday=abbreviations[lesson.weekday]
        ))
