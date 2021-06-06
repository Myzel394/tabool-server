from rest_framework import serializers

from ..teacher import DetailTeacherSerializer
from ....models import Student

__all__ = [
    "UserStudentSerializer"
]


class UserStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "class_number", "main_teacher"
        ]

    main_teacher = DetailTeacherSerializer()
