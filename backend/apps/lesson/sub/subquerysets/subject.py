from django.conf import settings
from django_common_utils.libraries.models import CustomQuerySetMixin

__all__ = [
    "SubjectQuerySet"
]


# noinspection PyTypeChecker
class SubjectQuerySet(CustomQuerySetMixin.QuerySet):
    pass
