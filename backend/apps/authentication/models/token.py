import random
import string
from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import BEFORE_CREATE, hook, LifecycleModel

if TYPE_CHECKING:
    from django.contrib.auth import get_user_model

__all__ = [
    "AccessToken"
]


class AccessToken(LifecycleModel):
    class Meta:
        verbose_name = _("Zugangszeichen")
        verbose_name_plural = _("Zugangszeichen")
    
    TOKEN_LENGTH = 255
    
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )  # type: get_user_model()
    
    token = models.CharField(
        verbose_name=_("Token"),
        blank=True,
        unique=True,
        max_length=TOKEN_LENGTH,
        editable=False,
    )  # type: str
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    @hook(BEFORE_CREATE)
    def _hook_create_token(self):
        tokens = set(self.__class__.objects.values_list("token", flat=True))
        
        while True:
            token = "".join(
                random.choices(
                    string.ascii_letters + string.digits,
                    k=self.TOKEN_LENGTH
                )
            )
            
            if token not in tokens:
                break
        
        self.token = token
