from typing import *

from django_common_utils.libraries.utils.text import create_short
from rest_framework import serializers

from apps.django.main.lesson.public.serializer_fields import CourseField
from apps.django.main.school_data.public.serializer_fields import RoomField
from apps.django.utils.serializers import RandomIDSerializerMixin
from ...models import Classtest

__all__ = [
    "ClasstestListSerializer", "ClasstestDetailSerializer"
]


class ClasstestListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Classtest
        fields = [
            "course", "targeted_date", "truncated_information", "id"
        ]
    
    course = CourseField()
    
    truncated_information = serializers.SerializerMethodField()
    
    def get_truncated_information(self, instance: Classtest) -> Optional[str]:
        return create_short(instance.information) if instance.information else None


class ClasstestDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Classtest
        fields = [
            "course", "room", "targeted_date", "information", "created_at", "id"
        ]
        read_only_fields = [
            "created_at"
        ]
    
    course = CourseField()
    room = RoomField(required=False)
