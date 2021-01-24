from apps.django.main.homework.sub.subserializers.homework.mixins import IsPrivateMixin
from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from apps.django.utils.serializers import UserRelationField
from .base import BaseHomeworkSerializer
from ..user_relations import UserHomeworkRelationSerializer

__all__ = [
    "DetailHomeworkSerializer"
]


class DetailHomeworkSerializer(BaseHomeworkSerializer, IsPrivateMixin):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "lesson", "due_date", "information", "type", "created_at", "id",
            
            "user_relation", "is_private",
        ]
    
    lesson = LessonField(detail=True)
    
    user_relation = UserRelationField(
        UserHomeworkRelationSerializer,
        default={
            "completed": False,
            "ignore": False
        }
    )
