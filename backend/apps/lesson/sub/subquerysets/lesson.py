from datetime import date as d_date
from typing import *

from django.conf import settings
from django_common_utils.libraries.models import CustomQuerySetMixin

from apps.utils.date import find_next_date_by_weekday

if TYPE_CHECKING:
    from ...models import Lesson, LessonData

__all__ = [
    "LessonQuerySet"
]


# noinspection PyTypeChecker
class LessonQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "LessonQuerySet":
        return self.filter(lesson_data__course__participants__in=[user])
    
    def create_automatically(
            self,
            *,
            lesson_data: "LessonData",
            date: Optional[d_date] = None,
            **kwargs
    ) -> "Lesson":
        return self.get_or_create(
            date=date or find_next_date_by_weekday(d_date.today(), lesson_data.weekday),
            lesson_data=lesson_data,
            **kwargs
        )[0]
