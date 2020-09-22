from rest_framework import serializers

__all__ = [
    "HomeworkBySubjectSerializer"
]


class HomeworkBySubjectSerializer(serializers.Serializer):
    subject = serializers.CharField()
