from rest_framework import serializers

from ....models import UserHomeworkRelation

__all__ = [
    "UserHomeworkRelationSerializer"
]


class UserHomeworkRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHomeworkRelation
        fields = [
            "completed", "ignored"
        ]
