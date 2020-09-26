from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ...models import AccessToken
from ...validators import email_not_in_use, token_exists, token_not_in_use

__all__ = [
    "LoginSerializer", "RegisterSerializer"
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
            user = User.objects.all().only("email").get(email=email)
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


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email", "first_name", "last_name", "token"
        ]
    
    token = serializers.CharField(
        validators=[token_exists, token_not_in_use],
        min_length=AccessToken.TOKEN_LENGTH
    )
    
    email = serializers.EmailField(
        validators=[email_not_in_use]
    )
    
    def create(self, validated_data):
        return User.objects.create_user(
            validated_data.pop("email"),
            validated_data.pop("password"),
            **validated_data
        )
