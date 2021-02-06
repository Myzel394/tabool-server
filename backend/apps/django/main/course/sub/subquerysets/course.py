from django.conf import settings
from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

__all__ = [
    "CourseQuerySet"
]


# noinspection PyTypeChecker
class CourseQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "CourseQuerySet":
        if user.is_teacher:
            return self \
                .only("teacher") \
                .filter(teacher=user.teacher)
        return self \
            .only("participants", "teacher") \
            .filter(participants__in=[user])
