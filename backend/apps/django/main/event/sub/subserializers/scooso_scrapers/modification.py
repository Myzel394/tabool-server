from apps.django.utils.serializers import GetOrCreateSerializerMixin
from ....models import Modification

__all__ = [
    "ModificationScoosoScraperSerializer"
]


class ModificationScoosoScraperSerializer(GetOrCreateSerializerMixin):
    class Meta:
        model = Modification
        fields = [
            "information", "modification_type", "start_datetime", "end_datetime"
        ]
    
    def create(self, validated_data):
        unique_data = {
            "lesson": validated_data.pop("lesson"),
            "start_datetime": validated_data.pop("start_datetime"),
            "end_datetime": validated_data.pop("end_datetime"),
        }
        instance = super().create(unique_data)
        other_data = {
            key: value
            for key, value in validated_data.items()
            if key not in unique_data
        }
        
        for key, value in other_data.items():
            setattr(instance, key, value)
        
        instance.save()
        
        return instance
