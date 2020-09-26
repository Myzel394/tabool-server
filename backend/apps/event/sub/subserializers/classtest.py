from rest_framework import serializers

from apps.lesson.public.serializer_fields import CourseField, RoomField
from apps.utils.serializers import RandomIDSerializerMixin
from ...models import Classtest

__all__ = [
    "ClasstestListSerializer", "ClasstestDetailSerializer"
]


class ClasstestListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Classtest
        fields = [
            "course", "id"
        ]
    
    course = CourseField()


class ClasstestDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Classtest
        fields = [
            "course", "room", "targeted_date", "information", "created_at", "edited_at", "id"
        ]
    
    course = CourseField()
    room = RoomField()
    edited_at = serializers.DateTimeField(read_only=True)
