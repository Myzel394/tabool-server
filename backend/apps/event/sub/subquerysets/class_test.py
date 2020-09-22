from django.conf import settings
from django_common_utils.libraries.models import CustomQuerySetMixin


class ClassTestQuerySetMixin(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "ClassTestQuerySetMixin":
        return self

# TODO: AssociatedUser zu Subject ändern!
