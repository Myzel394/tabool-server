import calendar
from typing import *

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from apps.django.main.timetable.models import Lesson

__all__ = [
    "validate_no_timetable_overlap"
]


def validate_no_timetable_overlap(value: "Lesson"):
    lessons = value.timetable.lessons
    overlaps_available = any(
        lesson.weekday == value.weekday and (
                (value.start_hour <= lesson.end_hour) and (value.end_hour >= lesson.start_hour)
                or (value.start_hour == lesson.start_hour and value.end_hour == lesson.end_hour)
        )
        for lesson in lessons
    )
    
    if overlaps_available:
        weekday_names = list(calendar.day_name)
        
        raise ValidationError(
            _("Es gibt Überlappungen mit der Stunde am {weekday} in der {start_hour} - {end_hour}. Stunde.").format(
                weekday=weekday_names[value.weekday],
                start_hour=value.start_hour,
                end_hour=value.end_hour
            )
        )
