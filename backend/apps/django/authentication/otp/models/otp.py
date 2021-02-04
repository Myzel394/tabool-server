import secrets
import string
from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import BEFORE_CREATE, hook

from apps.django.utils.models import AssociatedUserMixin, IdMixin
from .. import constants
from ..public import model_names

__all__ = [
    "OTP"
]


class OTP(IdMixin, AssociatedUserMixin):
    class Meta:
        verbose_name = model_names.OTP
        verbose_name_plural = model_names.OTP_PLURAL
        ordering = ("expire_date",)
    
    TOKEN_LENGTH = 6
    CHOICES = string.ascii_letters + string.digits
    
    token = models.CharField(
        max_length=TOKEN_LENGTH,
        verbose_name=_("Token")
    )
    
    expire_date = models.DateTimeField(
        verbose_name=_("Ablaufdatum"),
    )
    
    def is_valid(self, token: str) -> bool:
        return self.token == token
    
    @hook(BEFORE_CREATE)
    def _hook_create(self):
        self.token = "".join(
            secrets.choice(self.CHOICES)
            for _ in range(self.TOKEN_LENGTH)
        )
        self.expire_date = datetime.now() + timedelta(minutes=constants.OTP_EXPIRE_DURATION)
