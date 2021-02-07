from typing import *

from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

from apps.django.main.timetable.models import Lesson

if TYPE_CHECKING:
    from apps.django.authentication.user.models import User

__all__ = [
    "ModificationQuerySet"
]


# noinspection PyTypeChecker
class ModificationQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: "User") -> "ModificationQuerySet":
        lessons = Lesson.objects.from_user(user)
        
        return self.filter(lesson__in=lessons)
