from apps.django.main.lesson.models.classbook import Classbook
from apps.django.utils.serializers import GetOrCreateSerializerMixin

__all__ = [
    "ClassbookScoosoScraperSerializer"
]


class ClassbookScoosoScraperSerializer(GetOrCreateSerializerMixin):
    class Meta:
        model = Classbook
        fields = [
            "presence_content", "distance_content"
        ]
