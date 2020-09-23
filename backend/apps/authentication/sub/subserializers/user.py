from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from ...models import User


# TODO: Read_only fields zu serialiern hinzufügen! (generell über Meta informieren)
# TODO: Add field-level exceptions!


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
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


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email", "first_name", "last_name", "password", "id"
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "required": True
            },
            "email": {
                "required": True
            }
        }
    
    def create(self, validated_data):
        return User.objects.create_user(
            validated_data.pop("email"),
            validated_data.pop("password"),
            **validated_data
        )

