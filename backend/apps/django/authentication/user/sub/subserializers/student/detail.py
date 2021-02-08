from typing import *

from rest_framework import serializers

from .base import BaseStudentSerializer
from ..teacher import DetailTeacherSerializer

if TYPE_CHECKING:
    from ....models import Student

__all__ = [
    "DetailStudentSerializer"
]


class DetailStudentSerializer(BaseStudentSerializer):
    class Meta(BaseStudentSerializer.Meta):
        fields = [
            "main_teacher", "class_number", "first_name", "last_name", "gender", "email", "gender", "id"
        ]
    
    main_teacher = DetailTeacherSerializer()
    
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    
    @staticmethod
    def get_first_name(instance: "Student") -> str:
        return instance.user.first_name
    
    @staticmethod
    def get_last_name(instance: "Student") -> str:
        return instance.user.last_name
    
    @staticmethod
    def get_email(instance: "Student") -> str:
        return instance.user.email
    
    @staticmethod
    def get_id(instance: "Student") -> str:
        return instance.user.id
    
    @staticmethod
    def get_gender(instance: "Student") -> str:
        return instance.user.gender
