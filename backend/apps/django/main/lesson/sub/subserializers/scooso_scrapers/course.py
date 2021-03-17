from django.core.exceptions import ObjectDoesNotExist

from apps.django.main.authentication.models import Student
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
        subject = validated_data["subject"]
        course_number = validated_data["course_number"]
        teacher = validated_data["teacher"]
        
        participants = validated_data.pop("participants", [])
        
        try:
            students = Student.objects.filter(class_number=validated_data["class_number"])
            users = [
                student.user
                for student in students
            ]
            
            instance = Course.objects.get(
                subject=subject,
                course_number=course_number,
                teacher=teacher,
                participants__in=users
            )
        except ObjectDoesNotExist:
            instance = Course.objects.create(
                subject=subject,
                course_number=course_number,
                teacher=teacher,
            )
        
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
