from apps.django.authentication.user.public.serializer_fields.user import UserField
from apps.django.main.timetable.public.serializer_fields.lesson import LessonField
from .base import BaseHomeworkSerializer

__all__ = [
    "StudentCreateHomeworkSerializer", "TeacherCreateHomeworkSerializer"
]


class StudentCreateHomeworkSerializer(BaseHomeworkSerializer):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "due_date", "information", "type", "lesson", "lesson_date",
        ]
    
    lesson = LessonField()
    
    def create(self, validated_data):
        validated_data["private_to_user"] = self.context["request"].user
        
        return super().create(validated_data)


class TeacherCreateHomeworkSerializer(BaseHomeworkSerializer):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "due_date", "information", "type", "lesson", "lesson_date",
            
            "private_to_user"
        ]
    
    lesson = LessonField()
    private_to_user = UserField(required=False)
