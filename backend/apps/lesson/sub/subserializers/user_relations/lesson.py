from rest_framework import serializers

from ....models import UserLessonRelation

__all__ = [
    "UserLessonRelationSerializer"
]


class UserLessonRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLessonRelation
        fields = [
            "attendance"
        ]
