from datetime import date
from typing import *

from .models import Lesson, LessonData
from .utils import find_next_date_with_weekday

__all__ = [
    "lesson_data_to_lesson"
]


def lesson_data_to_lesson(
        *,
        lesson_data: LessonData,
        lesson_date: Optional[date] = None,
        **kwargs
) -> Lesson:
    return Lesson.objects.get_or_create(
        date=lesson_date or find_next_date_with_weekday(lesson_date, lesson_data.weekday),
        lesson_data=lesson_data,
        **kwargs
    )
