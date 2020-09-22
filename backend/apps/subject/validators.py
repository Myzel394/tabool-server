from datetime import date, datetime
from typing import *

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

if TYPE_CHECKING:
    from .models import LessonData

__all__ = [
    "validate_lesson_weekday"
]


def validate_lesson_weekday(actual_date: date, lesson: "LessonData"):
    if (weekday := actual_date.weekday()) != lesson.weekday:
        raise ValidationError(_(
            "Die Schulstunde kann an diesem Wochentag nicht stattfinden"
        ).format(weekday=weekday, lesson_weekday=lesson.weekday))
    
