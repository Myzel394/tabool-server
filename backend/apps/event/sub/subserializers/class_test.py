from rest_framework import serializers

from apps.lesson.public.serializer_fields import CourseField, RoomField
from apps.utils.serializers import RandomIDSerializerMixin
from ...models import ClassTest

__all__ = [
    "ClassTestListSerializer", "ClassTestDetailSerializer"
]


class ClassTestListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = ClassTest
        fields = [
            "course", "id"
        ]
    
    course = CourseField()


class ClassTestDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = ClassTest
        fields = [
            "course", "room", "targeted_date", "information", "created_at", "edited_at", "id"
        ]
    
    course = CourseField()
    room = RoomField()
    edited_at = serializers.DateTimeField(read_only=True)
