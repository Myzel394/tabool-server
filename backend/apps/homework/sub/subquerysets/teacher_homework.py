from .mixins.homework import BaseHomeworkQuerySetMixin

__all__ = [
    "TeacherHomeworkQuerySet"
]


# noinspection PyTypeChecker
class TeacherHomeworkQuerySet(BaseHomeworkQuerySetMixin):
    pass
