import secrets
import string

from django.db import models
from django_lifecycle import BEFORE_CREATE, hook, LifecycleModel

from ..public import model_names

__all__ = [
    "Preference"
]


class Preference(LifecycleModel):
    class Meta:
        verbose_name = model_names.PREFERENCE
        verbose_name_plural = model_names.PREFERENCE_PLURAL
        ordering = ("user",)
    
    id = models.CharField(
        max_length=8,
        primary_key=True,
        unique=True
    )
    
    data = models.TextField(
        max_length=16384 - 1,
        default="{}"
    )
    
    user = models.OneToOneField(
        "authentication.User",
        on_delete=models.CASCADE,
    )
    
    @hook(BEFORE_CREATE)
    def _hook_create_id(self):
        available_ids = set(self.__class__.objects.only("id").values_list("id", flat=True).distinct())
        while True:
            object_id = "".join(
                secrets.choice(string.ascii_letters + string.digits)
                for _ in range(8)
            )
            
            if object_id not in available_ids:
                break
        
        self.id = object_id
