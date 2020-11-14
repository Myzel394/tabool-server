from typing import *

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.django.extra.scooso_scraper.scrapers.request import LoginFailed, Request
from apps.django.main.school_data.public.serializer_fields.teacher import TeacherField
from ...models import ScoosoData, Student

if TYPE_CHECKING:
    from apps.django.main.authentication.models import User

__all__ = [
    "FullRegistrationSerializer", "ScoosoDataRegistrationSerializer", "StudentRegistrationSerializer"
]


class ScoosoDataRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoosoData
        fields = [
            "username", "password"
        ]
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Check if login is successful
        scraper = Request(username=attrs["username"], password=attrs["password"])
        try:
            scraper.login()
        except LoginFailed:
            raise ValidationError(
                _("Mit diesen Anmeldedaten konnte ich mich bei Scooso nicht anmelden.")
            )
        
        return data


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
    
    def _get_model(self, user: "User", model: Type[models.Model]) -> models.Model:
        try:
            return model.objects.only("user__id").get(user__id=user.id)
        except ObjectDoesNotExist:
            return model(user=user)
    
    def create(self, validated_data):
        # Preparation
        user = self.context["request"].user
        student = self._get_model(user, Student)
        scooso = self._get_model(user, ScoosoData)
        
        # Check
        student_serializer = StudentRegistrationSerializer(
            instance=student,
            data=validated_data["student"],
            context=self.context
        )
        student_serializer.is_valid(raise_exception=True)
        
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
