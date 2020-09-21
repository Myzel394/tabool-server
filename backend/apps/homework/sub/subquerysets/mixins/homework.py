from typing import *
from datetime import datetime, timedelta

from django.db.models import Q
from django_common_utils.libraries.models import CustomQuerySetMixin

if TYPE_CHECKING:
    from apps.subject.models import Subject

__all__ = [
    "BaseHomeworkQuerySetMixin"
]


# noinspection PyTypeChecker
class BaseHomeworkQuerySetMixin(CustomQuerySetMixin.QuerySet):
    def expired(self) -> "BaseHomeworkQuerySetMixin":
        return self.only("due_date").filter(
            Q(due_date=None) | Q(due_date__lte=datetime.now())
        )
    
    def not_expired(self) -> "BaseHomeworkQuerySetMixin":
        return self.only("due_date").filter(
            Q(due_date=None) | Q(due_date__gte=datetime.now())
        )
    
    def expires_today(self) -> "BaseHomeworkQuerySetMixin":
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        tomorrow = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0)
        
        return self.only("due_date").filter(
            Q(due_date=None) | Q(due_date__gte=datetime.now(), due_date__lte=tomorrow)
        )
    
    def completed(self) -> "BaseHomeworkQuerySetMixin":
        return self.only("completed").filter(completed=True)
    
    def not_completed(self) -> "BaseHomeworkQuerySetMixin":
        return self.only("completed").filter(completed=False)
    
    def with_information(self) -> "BaseHomeworkQuerySetMixin":
        return self.only("information").exclude(information="")
    
    def by_subject(self, subject: Subject) -> "BaseHomeworkQuerySetMixin":
        return self.filter(lesson__subject=subject)
