from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .student import StudentSerializer
from ... import constants
from ...models import AccessToken
from ...validators import email_not_in_use, token_exists, token_not_in_use

__all__ = [
    "LoginSerializer", "RegisterSerializer", "FullRegisterSerializer"
]

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs: dict):
        super().validate(attrs)
        
        email = attrs["email"]
        password = attrs["password"]
        
        # Check existence
        try:
            user = User.objects.only("email").get(email=email)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({
                "email": _("Die E-Mail ist falsch eingegeben.")
            })
        
        # Check password
        if not user.check_password(password):
            raise serializers.ValidationError({
                "password": _("Das Passwort ist falsch.")
            })
        
        # User is valid from here
        
        if not user.is_active:
            raise serializers.ValidationError(_("Dein Account ist noch nicht aktiviert."))
        
        return {"user": user}


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[email_not_in_use]
    )
    
    password = serializers.CharField(
        validators=[validate_password]
    )
    
    token = serializers.CharField(
        validators=[token_exists, token_not_in_use],
        min_length=constants.TOKEN_LENGTH
    )
    
    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"],
            validated_data["password"],
        )
        token = AccessToken.objects.get(token=validated_data["token"])
        token.user = user
        token.save()
        
        return user


class FullRegisterSerializer(serializers.Serializer):
    scooso_username = serializers.CharField()
    scooso_password = serializers.CharField()
    user = serializers.CharField()
    
    student = StudentSerializer()
