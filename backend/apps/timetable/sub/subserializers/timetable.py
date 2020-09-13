from typing import *

from apps.timetable.models import TimeTable
from apps.utils.serializers import IdMixinSerializer, NestedSerializerMixin
from . import LessonSerializer

__all__ = [
    "TimeTableSerializer"
]


class TimeTableSerializer(IdMixinSerializer, NestedSerializerMixin):
    class Meta:
        model = TimeTable
        fields = ["lessons", "designation", "id"]
    
    lessons = LessonSerializer(many=True)
    
    def create(self, validated_data: Dict[str, Any]):
        # Get values
        user = self.context['request'].user
        lessons_raw = validated_data["lessons"]
        designation_raw = validated_data.get("designation")
        
        lessons = self.create_nested(LessonSerializer, lessons_raw, many=True)
        
        timetable = TimeTable.objects.create_with_lessons(
            lessons=lessons,
            designation=designation_raw,
            associated_user=user
        )
        
        return timetable
