from .mixins import BaseHomeworkFilterSetMixin
from ...models import TeacherHomework

__all__ = [
    "TeacherHomeworkFilterSet"
]


class TeacherHomeworkFilterSet(BaseHomeworkFilterSetMixin):
    class Meta:
        model = TeacherHomework
        fields = {
            "due_date": ["lte", "gte"],
            "completed": ["exact"],
        }
