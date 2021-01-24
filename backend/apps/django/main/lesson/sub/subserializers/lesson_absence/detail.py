from .base import BaseLessonAbsenceSerializer
from ..lesson import LessonDetailEndpointSerializer

__all__ = [
    "DetailLessonAbsenceSerializer"
]


class DetailLessonAbsenceSerializer(BaseLessonAbsenceSerializer):
    class Meta(BaseLessonAbsenceSerializer.Meta):
        fields = BaseLessonAbsenceSerializer.Meta.fields + ["lesson"]
        read_only = ["lesson"]
    
    lesson = LessonDetailEndpointSerializer()
