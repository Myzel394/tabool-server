from rest_framework import serializers

from ...models import Choice

__all__ = [
    "ChoiceSerializer"
]


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = [
            "text", "color", "id"
        ]
