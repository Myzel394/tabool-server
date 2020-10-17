from apps.django.utils.serializers import GetOrCreateSerializerMixin
from ....models import Modification

__all__ = [
    "ModificationScoosoScraperSerializer"
]


class ModificationScoosoScraperSerializer(GetOrCreateSerializerMixin):
    class Meta:
        model = Modification
        fields = [
            "start_datetime", "end_datetime", "information"
        ]
