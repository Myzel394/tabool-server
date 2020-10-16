from django_filters import rest_framework as filters

from apps.event.models import Modification

__all__ = [
    "ModificationFilterSet"
]


class ModificationFilterSet(filters.FilterSet):
    class Meta:
        model = Modification
        fields = {
            "start_datetime": ["lte", "gte"],
            "end_datetime": ["lte", "gte"],
            "modification_type": ["iexact"]
        }
