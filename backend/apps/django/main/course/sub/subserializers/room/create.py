from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .base import BaseRoomSerializer
from ....models import Room
from ....validators import validate_place

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
