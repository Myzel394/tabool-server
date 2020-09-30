from rest_framework import serializers

from apps.lesson.models import SubjectScoosoData
from apps.lesson.public.serializer_fields import SubjectField

__all__ = [
    "SubjectScoosoDataSerializer"
]


class SubjectScoosoDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectScoosoData
        fields = [
            "code", "scooso_id", "subject"
        ]
    
    subject = SubjectField()

