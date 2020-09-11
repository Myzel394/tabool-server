from apps.utils.serializers import IdMixinSerializer

from . import LessonSerializer
from ..models import TimeTable

__all__ = [
    "TimeTableSerializer"
]


class TimeTableSerializer(IdMixinSerializer):
    class Meta:
        model = TimeTable
        fields = ["lessons", "designation", "id"]
    
    lessons = LessonSerializer(many=True)
