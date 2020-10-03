from rest_framework import serializers

from ....models import Modification

__all__ = [
    "ModificationScoosoScraperSerializer"
]


class ModificationScoosoScraperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modification
        fields = [
            "start_datetime", "end_datetime", "information"
        ]
