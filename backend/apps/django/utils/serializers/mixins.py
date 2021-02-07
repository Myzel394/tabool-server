from rest_framework import serializers

__all__ = [
    "GetOrCreateSerializerMixin",
]


class GetOrCreateSerializerMixin(serializers.ModelSerializer):
    def get_unique_fields(self, validated_data):
        return validated_data
    
    def create(self, validated_data):
        unique_data = self.get_unique_fields(validated_data)
        
        instance = self.Meta.model.objects.get_or_create(**unique_data)[0]
        self.update(instance, validated_data)
        
        return instance
