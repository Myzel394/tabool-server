from typing import *

from .base import BaseHomeworkSerializer

if TYPE_CHECKING:
    from ....models import Homework

__all__ = [
    "StudentUpdateHomeworkSerializer", "TeacherUpdateHomeworkSerializer"
]


class StudentUpdateHomeworkSerializer(BaseHomeworkSerializer):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "due_date", "information", "type",
        ]


class TeacherUpdateHomeworkSerializer(BaseHomeworkSerializer):
    instance: "Homework"
    
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "due_date", "information", "type"
        ]
