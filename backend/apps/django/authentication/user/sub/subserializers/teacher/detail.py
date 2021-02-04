from typing import *

from rest_framework import serializers

from .base import BaseTeacherSerializer

if TYPE_CHECKING:
    from ....models import Teacher

__all__ = [
    "DetailTeacherSerializer"
]


class DetailTeacherSerializer(BaseTeacherSerializer):
    class Meta(BaseTeacherSerializer.Meta):
        fields = [
            "first_name", "last_name", "short_name", "email", "gender", "id"
        ]
    
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    
    @staticmethod
    def get_first_name(instance: "Teacher") -> str:
        return instance.user.first_name
    
    @staticmethod
    def get_last_name(instance: "Teacher") -> str:
        return instance.user.last_name
