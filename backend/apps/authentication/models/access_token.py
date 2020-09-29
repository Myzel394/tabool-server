import random
import string
from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import CreationDateMixin, RandomIDMixin
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from .. import constants
from ..exceptions import CannotChangeTokenError
from ..querysets import AccessTokenQuerySet

if TYPE_CHECKING:
    from django.contrib.auth import get_user_model

__all__ = [
    "AccessToken"
]


class AccessToken(RandomIDMixin, CreationDateMixin, LifecycleModel):
    class Meta:
        verbose_name = _("Zugangszeichen")
        verbose_name_plural = _("Zugangszeichen")
        ordering = ("created_at",)
    
    objects = AccessTokenQuerySet()
    
    user = models.OneToOneField(
        "authentication.User",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )  # type: get_user_model()
    
    token = models.CharField(
        verbose_name=_("Token"),
        blank=True,
        unique=True,
        max_length=constants.TOKEN_LENGTH,
        editable=False,
    )  # type: str
    
    @hook(BEFORE_CREATE)
    def _hook_create_token(self):
        tokens = set(self.__class__.objects.values_list("token", flat=True))
        
        while True:
            token = "".join(
                random.choices(
                    string.ascii_letters + string.digits,
                    k=constants.TOKEN_LENGTH
                )
            )
            
            if token not in tokens:
                break
        
        self.token = token
    
    @hook(BEFORE_UPDATE, when="token")
    def _hook_prevent_token_change(self):
        if self.has_changed("token"):
            raise CannotChangeTokenError(_(
                "Der Zugangscode kann nicht geändert werden."
            ))
