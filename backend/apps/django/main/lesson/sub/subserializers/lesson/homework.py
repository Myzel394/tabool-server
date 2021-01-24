from rest_framework import serializers

from apps.django.main.homework.models import Homework
from apps.django.main.homework.sub.subserializers.homework.mixins import IsPrivateMixin
from apps.django.main.homework.sub.subserializers.user_relations import UserHomeworkRelationSerializer
from apps.django.utils.serializers import UserRelationField

__all__ = [
    "LessonHomeworkSerializer"
]


class LessonHomeworkSerializer(serializers.ModelSerializer, IsPrivateMixin):
    class Meta:
        model = Homework
        fields = [
            "due_date", "information", "type", "created_at", "id",
            
            "user_relation", "is_private",
        ]
    
    user_relation = UserRelationField(
        UserHomeworkRelationSerializer,
        default={
            "completed": False,
            "ignore": False
        }
    )
