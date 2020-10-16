from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.django.main.authentication.models.student import Student
from apps.django.main.school_data.public.serializer_fields import TeacherField

__all__ = [
    "StudentSerializer"
]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "class_number", "main_teacher", "user"
        ]
        read_only_fields = ["user"]
    
    main_teacher = TeacherField()
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        if hasattr(self.context["request"].user, "student"):
            raise ValidationError(_("Schüler können nur einmal pro Benutzer registriert werden."))
        
        return data
    
    def save(self, **kwargs):
        kwargs.setdefault("user", self.context["request"].user)
        
        return super().save(**kwargs)
