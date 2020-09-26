import random

from django.db import models
from django.utils.translation import gettext as _
from django_hint import *
from django_lifecycle import AFTER_CREATE, BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

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


class UserRelationMixin(LifecycleModel):
    class Meta:
        abstract = True
    
    RELATED_MODEL: StandardModelType
    
    @hook(AFTER_CREATE)
    def _user_relation_mixin_hook_create_relation(self):
        self.RELATED_MODEL.objects.create(**{
            self.__class__.__name__.lower(): self
        })
    
    @property
    def user_relation(self):
        return getattr(self, self.RELATED_MODEL.__name__.lower())
