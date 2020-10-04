from typing import *

from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

if TYPE_CHECKING:
    from apps.authentication.models import User

__all__ = [
    "MaterialQuerySet"
]


class MaterialQuerySet(CustomQuerySetMixin.QuerySet):
    def user_accessible(self, user: "User") -> "MaterialQuerySet":
        return self.filter(lesson__lesson_data__course__participants__in=[user])
