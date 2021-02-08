from apps.django.main.timetable.sub.subserializers.lesson import DetailLessonSerializer
from apps.django.utils.serializers import UserRelationField
from .base import BaseHomeworkSerializer
from ..user_relations import UserHomeworkRelationSerializer

__all__ = [
    "StudentDetailHomeworkSerializer", "TeacherDetailHomeworkSerializer"
]


class StudentDetailHomeworkSerializer(BaseHomeworkSerializer):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "due_date", "information", "type", "created_at", "id",
            "user_relation",
        ]
    
    lesson = DetailLessonSerializer()
    
    user_relation = UserRelationField(
        UserHomeworkRelationSerializer,
        default={
            "completed": False,
            "ignore": False
        }
    )


class TeacherDetailHomeworkSerializer(BaseHomeworkSerializer):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "due_date", "information", "type", "created_at", "id",
            "private_to_user",
        ]
    
    lesson = DetailLessonSerializer()
