from .base import BaseHomeworkSerializer

__all__ = [
    "StudentUpdateHomeworkSerializer", "TeacherUpdateHomeworkSerializer"
]


class StudentUpdateHomeworkSerializer(BaseHomeworkSerializer):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "due_date", "information", "type",
        ]


class TeacherUpdateHomeworkSerializer(BaseHomeworkSerializer):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "due_date", "information", "type",
        ]
