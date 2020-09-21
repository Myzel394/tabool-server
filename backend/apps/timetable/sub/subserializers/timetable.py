from typing import *

from apps.subject.sub.subserializers import LessonSerializer
from apps.timetable.models import TimeTable
from apps.utils.serializers import IdMixinSerializer, NestedModelSerializerField

__all__ = [
    "TimeTableSerializer"
]


class TimeTableSerializer(IdMixinSerializer):
    class Meta:
        model = TimeTable
        fields = ["lessons", "designation", "id"]
    
    lessons = NestedModelSerializerField(
        LessonSerializer,
        many=True
    )
    
    def create(self, validated_data: Dict[str, Any]):
        # Get values
        user = self.context['request'].user
        lessons = validated_data["lessons"]
        designation = validated_data.get("designation")
        
        timetable = TimeTable.objects.create_with_lessons(
            lessons=lessons,
            designation=designation,
            associated_user=user
        )
        
        return timetable
