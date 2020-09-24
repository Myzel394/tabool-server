from .mixins import BaseHomeworkFilterSetMixin
from ...models import UserHomework

__all__ = [
    "UserHomeworkFilterSet"
]


class UserHomeworkFilterSet(BaseHomeworkFilterSetMixin):
    class Meta:
        model = UserHomework
        fields = {
            "due_date": ["lte", "gte"],
            "completed": ["exact"],
            "homework_type": ["iexact"]
        }
