from django.db import models
from django_common_utils.libraries.models.mixins import CreationDateMixin, RandomIDMixin

__all__ = [
    "ScoosoRequest"
]


class ScoosoRequest(RandomIDMixin, CreationDateMixin):
    response = models.CharField(
        max_length=32_768 - 1,
    )
    
    name = models.CharField(
        max_length=255,
    )
