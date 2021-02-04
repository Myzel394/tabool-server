from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

__all__ = [
    "LoginSerializer"
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
        
        return {"user": user}
