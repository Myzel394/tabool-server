import random

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_lifecycle import BEFORE_CREATE, hook, LifecycleModel

from apps.django.utils.fields import ColorField
from ..constants import DEFAULT_COLOR_TEXT_MAPPING
from ..public import model_references
from ..public.model_names import CHOICE_NAME, CHOICE_NAME_PLURAL
from ..querysets import ChoiceQuerySet

__all__ = [
    "Choice"
]


def random_color() -> str:
    return "#" + "".join(random.choice("0123456789ABCDEF") for _ in range(6))


class Choice(RandomIDMixin, LifecycleModel):
    class Meta:
        verbose_name = CHOICE_NAME
        verbose_name_plural = CHOICE_NAME_PLURAL
        ordering = ("text",)
    
    objects = ChoiceQuerySet.as_manager()
    
    poll = models.ForeignKey(
        model_references.POLL,
        on_delete=models.CASCADE,
    )
    
    text = models.CharField(
        max_length=24,
        verbose_name=_("Text")
    )
    
    color = ColorField(
        verbose_name=_("Farbe"),
        blank=True,
    )
    
    @hook(BEFORE_CREATE)
    def _hook_create_color_if_none(self):
        self.color = self.color or DEFAULT_COLOR_TEXT_MAPPING.get(self.text.lower()) or random_color()
