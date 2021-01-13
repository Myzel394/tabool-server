from apps.django.utils.serializers import GetOrCreateSerializerMixin
from ....models import Course

__all__ = [
    "CourseScoosoScraperSerializer"
]


class CourseScoosoScraperSerializer(GetOrCreateSerializerMixin):
    class Meta:
        model = Course
        fields = [
            "course_number",
        ]
    
    def create(self, validated_data):
        participants = validated_data.pop("participants", [])
        instance: Course = super().create(validated_data)
        instance.participants.add(*participants)
        
        return instance
    
    def update(self, instance, validated_data):
        participants = validated_data.pop("participants", [])
        instance: Course = super().update(instance, validated_data)
        instance.participants.add(*participants)
        
        return instance
