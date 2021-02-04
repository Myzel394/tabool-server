from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import BEFORE_CREATE, hook

from apps.django.utils.models import AssociatedUserMixin, IdMixin
from .. import constants
from ..public import model_names

__all__ = [
    "KnownIp"
]


class KnownIp(IdMixin, AssociatedUserMixin):
    class Meta:
        verbose_name = model_names.KNOWN_IP
        verbose_name_plural = model_names.KNOWN_IP_PLURAL
    
    expire_date = models.DateTimeField(
        verbose_name=_("Ablaufdatum")
    )
    
    ip_address = models.GenericIPAddressField(
        verbose_name=_("Ip-Adresse")
    )
    
    @hook(BEFORE_CREATE)
    def _hook_create(self):
        self.expire_date = datetime.now() + timedelta(days=constants.REMEMBER_KNOWN_IP_DURATION)
