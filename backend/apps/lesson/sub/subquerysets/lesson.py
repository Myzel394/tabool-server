from datetime import date as d_date
from typing import *

from django.conf import settings
from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

from apps.utils.date import find_next_date_by_weekday
from apps.utils.querysets import RelationQuerySetMixin
from ...models.user_relations.lesson import UserLessonRelation

if TYPE_CHECKING:
    from ...models import Lesson, LessonData

__all__ = [
    "LessonQuerySet"
]


# noinspection PyTypeChecker
class LessonQuerySet(CustomQuerySetMixin.QuerySet, RelationQuerySetMixin):
    ref_filter_statement = "lesson_data__course"
    related_model = UserLessonRelation
    
    @staticmethod
    def get_ref_from_element(element: "Lesson"):
        return element.lesson_data.course
    
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
    
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "LessonQuerySet":
        return self.filter(lesson_data__course__participants__in=[user])
