from apps.django.main.homework.models import Homework

__all__ = [
    "HomeworkScoosoScraperSerializer"
]

from apps.django.utils.serializers import GetOrCreateSerializerMixin


class HomeworkScoosoScraperSerializer(GetOrCreateSerializerMixin):
    class Meta:
        model = Homework
        fields = [
            "information", "due_date"
        ]
    
    def get_unique_fields(self, validated_data):
        return {
            "lesson": validated_data.pop("lesson"),
        }
