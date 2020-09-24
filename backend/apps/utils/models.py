import random

from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from apps.authentication.public.model_references import USER
from apps.authentication.public.model_verbose_functions import user_single
from apps.utils.fields import ColorField
from constants import colors


class ColorMixin(LifecycleModel):
    class Meta:
        abstract = True
    
    color = ColorField(
        verbose_name=_("Farbe"),
        blank=True,
    )
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="color")
    def _hook_before_save_color(self):
        self.color = self.color or random.sample(colors.BEAUTIFUL_COLORS, 1)[0]


class AssociatedUserMixin(models.Model):
    class Meta:
        abstract = True
    
    associated_user = models.ForeignKey(
        USER,
        verbose_name=user_single,
        on_delete=models.CASCADE,
        editable=False
    )


class AddedAtMixin(models.Model):
    class Meta:
        abstract = True
    
    added_at = models.DateTimeField(
        verbose_name=_("Hinzugefügt"),
        blank=True,
        null=True
    )
