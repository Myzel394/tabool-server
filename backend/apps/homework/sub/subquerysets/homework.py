from .mixins.homework import BaseHomeworkQuerySetMixin

__all__ = [
    "HomeworkQuerySet"
]


class HomeworkQuerySet(BaseHomeworkQuerySetMixin, AddedAtMixin):
    pass
