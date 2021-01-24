from apps.django.main.homework.sub.subserializers.homework.mixins import IsPrivateMixin
from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from .base import BaseHomeworkSerializer

__all__ = [
    "CreateHomeworkSerializer"
]


class CreateHomeworkSerializer(BaseHomeworkSerializer, IsPrivateMixin):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "due_date", "information", "type", "lesson",
            
            "is_private"
        ]
    
    lesson = LessonField()
    
    def create(self, validated_data):
        validated_data["private_to_user"] = self.get_private_to_user()
        
        return super().create(validated_data)
