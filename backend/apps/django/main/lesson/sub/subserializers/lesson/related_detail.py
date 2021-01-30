from rest_framework import serializers

from apps.django.main.school_data.public.serializer_fields.room import RoomField
from ..classbook import ClassbookSerializer
from ....models import Lesson
from ....public.serializer_fields.course import CourseField

__all__ = [
    "RelatedDetailLessonSerializer"
]


class RelatedDetailLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "room", "course", "start_time", "end_time", "weekday",
            "date", "id", "classbook", "video_conference_link"
        ]
    
    classbook = ClassbookSerializer()
    
    course = CourseField(detail=True)
    room = RoomField(required=False, detail=True)
