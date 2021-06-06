from typing import *

from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

from apps.django.main.course.models import Course

if TYPE_CHECKING:
    from apps.django.authentication.user.models import User

__all__ = [
    "ExamQuerySet"
]


# noinspection PyTypeChecker
class ExamQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: "User") -> "ExamQuerySet":
        courses = Course.objects.from_user(user)

        return self.filter(course__in=courses)
