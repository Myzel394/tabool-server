from rest_framework import serializers

from ....models import UserEventRelation

__all__ = [
    "UserEventRelationSerializer"
]


class UserEventRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEventRelation
        fields = [
            "ignore"
        ]
