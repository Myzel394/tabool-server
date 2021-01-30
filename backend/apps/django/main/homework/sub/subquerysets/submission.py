from typing import *

from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

if TYPE_CHECKING:
    from apps.django.main.authentication.models import User

__all__ = [
    "SubmissionQuerySet"
]


class SubmissionQuerySet(CustomQuerySetMixin.QuerySet):
    def user_accessible(self, user: "User") -> "SubmissionQuerySet":
        return self.filter(lesson__course__participants__in=[user])
