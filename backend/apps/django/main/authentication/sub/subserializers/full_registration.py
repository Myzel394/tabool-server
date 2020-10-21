from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.django.main.school_data.public.serializer_fields import TeacherField
from ...models import ScoosoData, Student

__all__ = [
    "FullRegistrationSerializer"
]


class ScoosoDataRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoosoData
        fields = [
            "username", "password"
        ]


class StudentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "class_number", "main_teacher"
        ]
    
    main_teacher = TeacherField(label=_("Klassenlehrer/Stammkursleiter"))


class FullRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["student", "scoosodata"]
    
    student = serializers.DictField(write_only=True)
    scoosodata = serializers.DictField(write_only=True)
    
    def create(self, validated_data):
        # Preparation
        user = self.context["request"].user
        
        # Check
        student = getattr(user, "student", Student(user=user))
        student_serializer = StudentRegistrationSerializer(
            instance=student,
            data=validated_data["student"],
            context=self.context
        )
        student_serializer.is_valid(raise_exception=True)
        
        scooso = getattr(user, "scoosodata", ScoosoData(user=user))
        scooso_serializer = ScoosoDataRegistrationSerializer(
            instance=scooso,
            data=validated_data["scoosodata"],
            context=self.context
        )
        scooso_serializer.is_valid(raise_exception=True)
        
        # Action
        student_serializer.save()
        scooso_serializer.save()
        
        user.has_filled_out_data = True
        user.save()
        
        return user
