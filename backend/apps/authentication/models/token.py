import random
import string

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins.common import RandomIDMixin
from django_common_utils.libraries.models.mixins.date import CreationDateMixin
from django_lifecycle import BEFORE_CREATE, hook

from apps.utils.model_verbose_functions import user_single


# TODO: Creation date zu verschiedenen Modeln hinzufügen

__all__ = [
    "AccessToken"
]


class AccessToken(RandomIDMixin, CreationDateMixin):
    class Meta:
        verbose_name = _("Zugangszeichen")
        verbose_name_plural = _("Zugangszeichen")

    TOKEN_LENGTH = 255

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=user_single,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    token = models.CharField(
        verbose_name=_("Token"),
        blank=True,
        unique=True,
        max_length=TOKEN_LENGTH,
        editable=False,
    )
    
    @hook(BEFORE_CREATE)
    def _hook_create_token(self):
        while True:
            token = "".join(
                random.choices(
                    string.ascii_letters + string.digits,
                    k=self.TOKEN_LENGTH
                )
            )
            
            if not self.objects.only("token").filter(token=token).exists():
                break
        
        self.token = token

