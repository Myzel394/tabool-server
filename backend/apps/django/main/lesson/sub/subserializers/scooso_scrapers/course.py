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
        unique_data = {
            "subject": validated_data.pop("subject"),
            "course_number": validated_data.pop("course_number"),
        }
        
        participants = validated_data.pop("participants", [])
        instance: Course = super().create(unique_data)
        instance.participants.add(*participants)
        
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        instance.save()
        
        return instance
    
    def update(self, instance, validated_data):
        participants = validated_data.pop("participants", [])
        instance: Course = super().update(instance, validated_data)
        instance.participants.add(*participants)
        
        return instance
