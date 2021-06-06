from datetime import datetime

from django.conf import settings
from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

from apps.django.main.timetable.models import Lesson

__all__ = [
    "SubmissionQuerySet"
]


# noinspection PyTypeChecker
class SubmissionQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "SubmissionQuerySet":
        lessons = Lesson.objects.from_user(user)
        qs = self \
            .only("lesson") \
            .filter(lesson__in=lessons)

        if user.is_teacher:
            qs = qs \
                .only("publish_datetime") \
                .filter(publish_datetime__lte=datetime.now()) \
                .distinct()

        return qs
