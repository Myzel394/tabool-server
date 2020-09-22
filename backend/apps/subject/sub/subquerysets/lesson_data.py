from datetime import date
from typing import *

from django.conf import settings
from django_common_utils.libraries.models import CustomQuerySetMixin

from ...models import Lesson
from ...utils import find_next_date_with_weekday

if TYPE_CHECKING:
    from ...models import LessonData


__all__ = [
    "LessonDataQuerySet"
]


# noinspection PyTypeChecker
class LessonDataQuerySet(CustomQuerySetMixin.QuerySet):
    @staticmethod
    def get_or_create_lesson(
            *,
            lesson_data: "LessonData",
            lesson_date: Optional["date"] = None,
            **kwargs
    ) -> "Lesson":
        return Lesson.objects.get_or_create(
            date=lesson_date or find_next_date_with_weekday(lesson_date, lesson_data),
            lesson_data=lesson_data,
            **kwargs
        )
        
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "LessonDataQuerySet":
        return self.only("associated_user").filter(associated_user=user)
    

