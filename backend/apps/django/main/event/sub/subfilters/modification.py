from django_common_utils.libraries.utils import model_verbose
from django_filters import rest_framework as filters

from apps.django.main.event.models import Modification
from apps.django.main.lesson.models import Lesson

__all__ = [
    "ModificationFilterSet"
]


class ModificationFilterSet(filters.FilterSet):
    class Meta:
        model = Modification
        fields = {
            "modification_type": ["iexact"]
        }
    
    lesson = filters.CharFilter(
        field_name="lesson__id",
        label=model_verbose(Lesson)
    )
