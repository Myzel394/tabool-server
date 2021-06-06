from datetime import datetime

from django.conf import settings
from django.db.models import Q
from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

from apps.django.main.timetable.models import Lesson

__all__ = [
    "MaterialQuerySet"
]


# noinspection PyTypeChecker
class MaterialQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "MaterialQuerySet":
        lessons = Lesson.objects.from_user(user)
        qs = self \
            .only("lesson") \
            .filter(lesson__in=lessons)

        if user.is_student:
            qs = qs \
                .only("publish_datetime", "announce") \
                .filter(Q(publish_datetime__lte=datetime.now(), announce=False) | Q(announce=True)) \
                .distinct()

        return qs
