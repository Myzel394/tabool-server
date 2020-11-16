from apps.django.utils.serializers import GetOrCreateSerializerMixin
from ....models import Modification

__all__ = [
    "ModificationScoosoScraperSerializer"
]


class ModificationScoosoScraperSerializer(GetOrCreateSerializerMixin):
    class Meta:
        model = Modification
        fields = [
            "information", "modification_type"
        ]
    
    def create(self, validated_data):
        unique_data = {
            "lesson": validated_data.pop("lesson"),
            "modification_type": validated_data.pop("modification_type")
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
