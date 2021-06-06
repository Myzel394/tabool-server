from typing import *

from rest_framework import serializers

from .base import BaseUserSerializer
from .student import UserStudentSerializer
from .teacher import UserTeacherSerializer
from ..preference import DetailPreferenceSerializer

if TYPE_CHECKING:
    from apps.django.authentication.user.models import User

__all__ = [
    "DetailUserSerializer", "UserInformationSerializer"
]


class DetailUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "first_name", "last_name", "email", "id"
        ]


class UserInformationSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "preference", "first_name", "last_name", "email", "id", "user_type", "gender",
            "student", "teacher"
        ]

    preference = DetailPreferenceSerializer()
    student = serializers.SerializerMethodField()
    teacher = serializers.SerializerMethodField()

    @staticmethod
    def get_student(instance: "User") -> Optional[dict]:
        if instance.is_student:
            return UserStudentSerializer(instance=instance.student).data

    @staticmethod
    def get_teacher(instance: "User") -> Optional[dict]:
        if instance.is_teacher:
            return UserTeacherSerializer(instance=instance.teacher).data
