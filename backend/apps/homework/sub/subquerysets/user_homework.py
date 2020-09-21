from apps.utils.models import AddedAtMixin, AssociatedUserMixin
from .mixins.homework import BaseHomeworkQuerySetMixin

__all__ = [
    "UserHomeworkQuerySet"
]


class UserHomeworkQuerySet(BaseHomeworkQuerySetMixin):
    pass
