from typing import *

from django.db import models
from rest_framework import serializers


class IdMixinSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        read_only=True,
    )

