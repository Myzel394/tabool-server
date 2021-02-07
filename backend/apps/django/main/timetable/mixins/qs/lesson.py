from datetime import date
from typing import *

from django.core.exceptions import ObjectDoesNotExist
from django_hint import QueryType

if TYPE_CHECKING:
    from ...models import Lesson

__all__ = [
    "get_via_referenced_lesson_date", "get_via_referenced_lesson_date_range"
]

T = TypeVar("T")


def get_via_referenced_lesson_date(
        qs: QueryType[T],
        lesson: "Lesson",
        lesson_date: date,
        many: bool = False
) -> Union[T, QueryType[T], None]:
    if many:
        return qs \
            .only("lesson", "lesson_date") \
            .filter(lesson=lesson, lesson_date=lesson_date)
    
    try:
        instance = qs \
            .only("lesson", "lesson_date") \
            .get(lesson=lesson, lesson_date=lesson_date)
    except ObjectDoesNotExist:
        return None
    
    return instance


def get_via_referenced_lesson_date_range(
        qs: QueryType[T],
        start_date: date,
        end_date: date,
        many: bool = True,
        **kwargs,
) -> Union[T, QueryType[T], None]:
    if many:
        return qs \
            .only("lesson_date", *kwargs.keys()) \
            .filter(lesson_date__gte=start_date, lesson_date__lte=end_date, **kwargs)
    
    try:
        instance = qs \
            .only("lesson_date", *kwargs.keys()) \
            .get(lesson_date__gte=start_date, lesson_date__lte=end_date, **kwargs)
    except ObjectDoesNotExist:
        return None
    
    return instance
