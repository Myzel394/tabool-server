from rest_framework import serializers

from apps.django.utils.serializers import RandomIDSerializerMixin
from ...models import Teacher
from ...public.serializer_fields import SubjectField

__all__ = [
    "TeacherListSerializer", "TeacherDetailSerializer"
]


class TeacherListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Teacher
        fields = ["short_name", "last_name", "id"]


class TeacherDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Teacher
        fields = [
            "first_name", "last_name", "short_name", "email", "teaches_subjects", "id"
        ]
    
    teaches_subjects = serializers.ListField(child=SubjectField())
