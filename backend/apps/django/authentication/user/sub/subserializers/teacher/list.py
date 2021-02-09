from rest_framework import serializers

from ....models import Teacher

__all__ = [
    "ListTeacherSerializer"
]


class ListTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            "short_name", "last_name", "gender", "id"
        ]
    
    last_name = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    
    @staticmethod
    def get_last_name(instance: "Teacher") -> str:
        return instance.user.last_name
    
    @staticmethod
    def get_id(instance: "Teacher") -> str:
        return instance.user.id
    
    @staticmethod
    def get_gender(instance: "Teacher") -> str:
        return instance.user.gender
