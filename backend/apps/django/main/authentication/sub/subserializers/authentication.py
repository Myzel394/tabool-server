from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ... import constants
from ...models import Token
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
            user = User.objects.only("email").get(email=email)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({
                "email": _("Diese E-Mail ist ungültig.")
            })
        
        # Check password
        if not user.check_password(password):
            raise serializers.ValidationError({
                "password": _("Das Passwort ist falsch.")
            })
        
        if not user.is_active:
            raise serializers.ValidationError(_("Dein Account wurde deaktiviert."))
        
        if user.is_being_setup:
            raise serializers.ValidationError(_("Dein Account wird noch erstellt, dies dauert ein bisschen."))
        
        return {"user": user}


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[email_not_in_use]
    )
    
    password = serializers.CharField(
        validators=[validate_password],
        style={"input_type": "password"}
    )
    
    token = serializers.CharField(
        validators=[token_exists, token_not_in_use],
        min_length=constants.TOKEN_LENGTH,
        max_length=constants.TOKEN_LENGTH,
        help_text=_("Dein Zugangscode, damit wir wissen, dass nur Schüler die App verwenden.")
    )
    
    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"],
            validated_data["password"],
        )
        token = Token.objects.get(token=validated_data["token"])
        token.user = user
        token.save()
        
        return user
