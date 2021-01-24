from apps.django.main.homework.sub.subserializers.homework.mixins import IsPrivateMixin
from .base import BaseHomeworkSerializer

__all__ = [
    "UpdateHomeworkSerializer"
]


class UpdateHomeworkSerializer(IsPrivateMixin, BaseHomeworkSerializer):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "due_date", "information", "type",
            
            "is_private"
        ]
    
    def update(self, instance, validated_data):
        validated_data["private_to_user"] = self.get_private_to_user()
        
        return super().update(instance, validated_data)
