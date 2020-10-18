import random
import string
from typing import *

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import CreationDateMixin, RandomIDMixin
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from .. import constants
from ..public import model_names
from ..querysets import AccessTokenQuerySet

if TYPE_CHECKING:
    from django.contrib.auth import get_user_model

__all__ = [
    "AccessToken"
]


class AccessToken(RandomIDMixin, CreationDateMixin, LifecycleModel):
    class Meta:
        verbose_name = model_names.TOKEN
        verbose_name_plural = model_names.TOKEN_PLURAL
        ordering = ("created_at",)
    
    objects = AccessTokenQuerySet()
    
    user = models.OneToOneField(
        "authentication.User",
        on_delete=models.CASCADE,
        verbose_name=model_names.USER,
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
    
    def __str__(self):
        return _("{user} vom {creation_date}").format(user=self.user, creation_date=self.created_at)
    
    def clean(self):
        if self.has_changed("token"):
            raise ValidationError(_(
                "Der Zugangscode kann nicht geändert werden."
            ))
        return super().clean()
    
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
    
    @hook(BEFORE_UPDATE, when="token", has_changed=True)
    def _hook_full_clean(self):
        self.full_clean()
