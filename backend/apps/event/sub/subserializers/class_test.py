from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from apps.subject.sub.subserializers import RoomDetailSerializer, SubjectDetailSerializer
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
        read_only_fields = ["id"]
    
    subject = SubjectDetailSerializer()


class ClassTestDetailSerializer(WritableNestedModelSerializer):
    class Meta:
        model = ClassTest
        fields = [
            "subject", "targeted_date", "information", "room", "id"
        ]
        read_only_fields = ["id"]
    
    subject = SubjectDetailSerializer()
    room = RoomDetailSerializer()
