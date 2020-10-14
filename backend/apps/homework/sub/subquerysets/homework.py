from datetime import datetime, timedelta
from typing import *

from django.conf import settings
from django.db.models import Q
from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

from apps.utils.querysets import RelationQuerySetMixin
from ...models.user_relations.homework import UserHomeworkRelation

if TYPE_CHECKING:
    from ...models import Homework
    from apps.school_data.models import Subject

__all__ = [
    "HomeworkQuerySet"
]


# noinspection PyTypeChecker
class HomeworkQuerySet(CustomQuerySetMixin.QuerySet, RelationQuerySetMixin):
    ref_filter_statement = "lesson__lesson_data__course"
    related_model = UserHomeworkRelation
    
    @staticmethod
    def get_ref_from_element(element: "Homework"):
        return element.lesson.lesson_data.course
    
    def expired(self) -> "HomeworkQuerySet":
        return self.only("due_date").filter(
            Q(due_date=None) | Q(due_date__lte=datetime.now())
        )
    
    def not_expired(self) -> "HomeworkQuerySet":
        return self.only("due_date").filter(
            Q(due_date=None) | Q(due_date__gte=datetime.now())
        )
    
    def expires_today(self) -> "HomeworkQuerySet":
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        tomorrow = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0)
        
        return self.only("due_date").filter(
            Q(due_date=None) | Q(due_date__gte=datetime.now(), due_date__lte=tomorrow)
        )
    
    def completed(self) -> "HomeworkQuerySet":
        return self.only("completed").filter(completed=True)
    
    def not_completed(self) -> "HomeworkQuerySet":
        return self.only("completed").filter(completed=False)
    
    def with_information(self) -> "HomeworkQuerySet":
        return self.only("information").exclude(information="")
    
    def by_subject(self, subject: "Subject") -> "HomeworkQuerySet":
        return self.filter(lesson__subject=subject)
    
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "HomeworkQuerySet":
        return self.filter(
            Q(lesson__lesson_data__course__participants__in=[user], private_to_user=None)
            | Q(private_to_user=user)
        )
