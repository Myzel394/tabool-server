import random
from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_lifecycle import BEFORE_SAVE, hook, LifecycleModel

from apps.django.utils.models import AssociatedUserMixin
from .. import constants
from ..public import model_names

__all__ = [
    "OTP"
]


class OTP(RandomIDMixin, AssociatedUserMixin, LifecycleModel):
    class Meta:
        verbose_name = model_names.OTP
        verbose_name_plural = model_names.OTP_PLURAL
        ordering = ("expire_date",)
    
    TOKEN_LENGTH = 6
    
    token = models.CharField(
        max_length=TOKEN_LENGTH,
        verbose_name=_("Token")
    )
    
    expire_date = models.DateTimeField(
        verbose_name=_("Ablaufdatum"),
    )
    
    def is_valid(self, token: str) -> bool:
        return self.token == token
    
    @hook(BEFORE_SAVE)
    def _hook_create(self):
        min_value = int("1" + "0" * (self.TOKEN_LENGTH - 1))
        max_value = int("9" * self.TOKEN_LENGTH)
        
        self.token = random.randint(min_value, max_value)
        self.expire_date = datetime.now() + timedelta(constants.OTP_EXPIRE_DURATION)
