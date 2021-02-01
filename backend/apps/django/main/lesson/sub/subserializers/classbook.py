from apps.django.main.lesson.models.classbook import Classbook
from apps.django.utils.serializers import RandomIDSerializerMixin

__all__ = [
    "ClassbookSerializer"
]


class ClassbookSerializer(RandomIDSerializerMixin):
    preferred_id_key = "classbook"
    
    class Meta:
        model = Classbook
        fields = [
            "presence_content", "distance_content",
        ]
