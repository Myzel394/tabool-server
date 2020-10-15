from django.db import models
from django.utils.translation import gettext_lazy as _
from django_bleach.models import BleachField
from django_common_utils.libraries.handlers.mixins import HTMLOptimizerHandler, TextOptimizerHandler
from django_common_utils.libraries.handlers.models import HandlerMixin
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_common_utils.libraries.models.mixins.date import EditCreationDateMixin
from django_eventstream import send_event
from django_lifecycle import AFTER_CREATE, hook, LifecycleModel

from apps.authentication.public import *
from apps.news.public.event_channels import NEWS_CHANNEL
from constants import maxlength

__all__ = [
    "News"
]


class News(RandomIDMixin, HandlerMixin, EditCreationDateMixin, LifecycleModel):
    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ("-created_at", "-edited_at", "title")
    
    title = models.CharField(
        max_length=maxlength.TITLE,
        verbose_name=_("Titel")
    )
    
    html = BleachField(
        verbose_name=_("HTML"),
    )
    
    author = models.ForeignKey(
        USER,
        verbose_name=user_single,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    
    @staticmethod
    def handlers():
        return {
            "html": HTMLOptimizerHandler(),
            "title": TextOptimizerHandler()
        }
    
    @hook(AFTER_CREATE)
    def _hook_send_event(self):
        send_event(NEWS_CHANNEL, "news", {})
