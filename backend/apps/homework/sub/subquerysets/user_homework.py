from .mixins.homework import BaseHomeworkQuerySetMixin

__all__ = [
    "UserHomeworkQuerySet"
]


class UserHomeworkQuerySet(BaseHomeworkQuerySetMixin):
    pass
