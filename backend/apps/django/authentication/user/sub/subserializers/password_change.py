from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.django.utils.serializers import ValidationSerializer

User = get_user_model()

__all__ = [
    "PasswordChangerSerializer"
]


class PasswordChangerSerializer(ValidationSerializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    
    def validate(self, attrs: dict):
        user: User = self.context["request"].user
        old_password: str = attrs["old_password"]
        new_password: str = attrs["new_password"]
        
        # Check passwords are the same
        if old_password == new_password:
            raise serializers.ValidationError({
                "new_password": _("Das Passwort ist das gleiche wie das alte!")
            })
        
        # Check password valid
        if not user.check_password(old_password):
            raise serializers.ValidationError({
                "old_password": _("Das Passwort ist falsch!")
            })
        
        return super().validate(attrs)
