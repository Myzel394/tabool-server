from rest_framework import serializers

from apps.django.main.school_data.public.serializer_fields.subject import SubjectField
from apps.django.main.school_data.public.serializer_fields.teacher import TeacherField
from apps.django.utils.serializers import PreferredIdsMixin, RandomIDSerializerMixin
from ...models import Course, LessonData

__all__ = [
    "CourseListSerializer", "CourseDetailSerializer"
]


class CourseListSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "course"
    
    class Meta:
        model = Course
        fields = [
            "subject", "teacher", "course_number", "id"
        ]
    
    subject = SubjectField(detail=True)
    teacher = TeacherField(detail=True)


class CourseDetailSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "course"
    
    class Meta:
        model = Course
        fields = [
            "subject", "teacher", "course_number", "participants_count", "weekdays", "id"
        ]
    
    subject = SubjectField(detail=True)
    teacher = TeacherField(detail=True)
    
    participants_count = serializers.SerializerMethodField()
    
    weekdays = serializers.SerializerMethodField()
    
    @staticmethod
    def get_participants_count(obj: Course):
        return obj.participants.all().count()
    
    def get_weekdays(self, instance: Course):
        return list(set(
            LessonData.objects
                .only("course")
                .filter(course=instance)
                .values_list("weekday", flat=True)
        ))
