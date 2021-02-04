from rest_framework import serializers

from ....models import UserSubjectRelation

__all__ = [
    "UserSubjectRelationSerializer"
]


class UserSubjectRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubjectRelation
        fields = [
            "color"
        ]
