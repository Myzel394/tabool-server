from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.django.main.school_data.models import Room
from apps.django.utils.validators import validate_place
from .base import BaseRoomSerializer

__all__ = [
    "CreateRoomSerializer"
]


class CreateRoomSerializer(BaseRoomSerializer):
    class Meta(BaseRoomSerializer.Meta):
        fields = [
            "place"
        ]
    
    place = serializers.CharField(
        # TODO: Make UniqueValidator as function!
        validators=[validate_place, UniqueValidator(queryset=Room.objects.all())],
    )
