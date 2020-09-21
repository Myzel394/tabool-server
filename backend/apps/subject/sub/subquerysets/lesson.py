from django.conf import settings
from django_common_utils.libraries.models import CustomQuerySetMixin


class LessonQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "LessonQuerySet":
        return self.only("associated_user").filter(associated_user=user)
