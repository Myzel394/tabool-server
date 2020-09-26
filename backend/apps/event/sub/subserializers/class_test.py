from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from apps.lesson.sub.subserializers import RoomDetailSerializer, SubjectDetailSerializer
from ...models import ClassTest

__all__ = [
    "ClassTestListSerializer", "ClassTestDetailSerializer"
]


class ClassTestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassTest
        fields = [
            "subject", "targeted_date", "id"
        ]
    
    subject = SubjectDetailSerializer()


class ClassTestDetailSerializer(WritableNestedModelSerializer):
    class Meta:
        model = ClassTest
        fields = [
            "subject", "targeted_date", "information", "created_at", "edited_at", "room", "id"
        ]
    
    subject = SubjectDetailSerializer()
    room = RoomDetailSerializer()
    edited_at = serializers.DateTimeField(read_only=True)
