from .base import BaseLessonAbsenceSerializer

__all__ = [
    "UpdateLessonAbsenceSerializer"
]


class UpdateLessonAbsenceSerializer(BaseLessonAbsenceSerializer):
    class Meta(BaseLessonAbsenceSerializer.Meta):
        fields = ["reason", "is_signed"]
