from django.db import models
from django.utils.translation import gettext_lazy as _
from django_bleach.models import BleachField
from django_common_utils.libraries.handlers.mixins import HTMLOptimizerHandler, TextOptimizerHandler
from django_common_utils.libraries.handlers.models import HandlerMixin
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_common_utils.libraries.models.mixins.date import EditCreationDateMixin
from django_lifecycle import LifecycleModel

from apps.django.authentication.user.public import *
from apps.django.extra.news.public import *

__all__ = [
    "News"
]


class News(RandomIDMixin, HandlerMixin, EditCreationDateMixin, LifecycleModel):
    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ("-created_at", "-edited_at", "title")

    title = models.CharField(
        max_length=127,
        verbose_name=_("Titel")
    )

    html = BleachField(
        verbose_name=_("HTML"),
    )

    author = models.ForeignKey(
        USER,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title

    @staticmethod
    def handlers():
        return {
            "html": HTMLOptimizerHandler(),
            "title": TextOptimizerHandler()
        }
