import random
from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

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
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False
    )


class DatesMixin(LifecycleModel):
    class Meta:
        abstract = True
    
    created_at = models.DateTimeField(
        verbose_name=_("Erstelldatum"),
        blank=True,
    )
    
    last_edited_at = models.DateTimeField(
        verbose_name=_("Zuletzt editiert"),
        blank=True,
        null=True
    )
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE)
    def _hook_set_created_at(self):
        self.created_at = datetime.now()
    
    @hook(BEFORE_UPDATE)
    def _hook_set_edited_at(self):
        self.last_edited_at = datetime.now()
