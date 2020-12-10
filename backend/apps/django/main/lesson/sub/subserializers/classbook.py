from apps.django.main.lesson.models.classbook import Classbook
from apps.django.utils.serializers import PreferredIdsMixin, RandomIDSerializerMixin

__all__ = [
    "ClassbookDetailSerializer"
]


class ClassbookDetailSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "classbook"
    
    class Meta:
        model = Classbook
        fields = [
            "presence_content", "distance_content",
        ]
