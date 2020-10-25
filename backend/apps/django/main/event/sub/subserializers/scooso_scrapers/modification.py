from apps.django.utils.serializers import GetOrCreateSerializerMixin
from ....models import Modification

__all__ = [
    "ModificationScoosoScraperSerializer"
]


class ModificationScoosoScraperSerializer(GetOrCreateSerializerMixin):
    class Meta:
        model = Modification
        fields = [
            "start_datetime", "end_datetime", "information", "modification_type"
        ]
    
    def create(self, validated_data):
        unique_data = {
            "start_datetime": validated_data.pop("start_datetime"),
            "end_datetime": validated_data.pop("end_datetime"),
            "course": validated_data.pop("course"),
            "modification_type": validated_data.pop("modification_type")
        }
        instance = super().create(unique_data)
        
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        instance.save()
        
        return instance
