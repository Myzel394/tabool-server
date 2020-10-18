import random

from django.db import models
from django.utils.translation import gettext as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from apps.django.main.authentication.public import *
from apps.django.main.authentication.public import model_names as auth_names
from apps.django.utils.fields.color import ColorField
from constants import colors

__all__ = [
    "ColorMixin", "AssociatedUserMixin", "AddedAtMixin", "UserModelRelationMixin", "ScoosoDataMixin"
]


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
        on_delete=models.CASCADE,
        verbose_name=auth_names.USER
    )


class AddedAtMixin(models.Model):
    class Meta:
        abstract = True
    
    added_at = models.DateTimeField(
        verbose_name=_("Hinzugefügt"),
        blank=True,
        null=True
    )


class UserModelRelationMixin(models.Model):
    class Meta:
        abstract = True
    
    user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        verbose_name=auth_names.USER
    )


class ScoosoDataMixin(RandomIDMixin):
    class Meta:
        abstract = True
    
    scooso_id = models.PositiveIntegerField(
        verbose_name=_("Scooso-ID"),
        blank=True,
        null=True
    )
