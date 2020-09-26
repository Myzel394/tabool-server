from django.db import models
from django.utils.translation import gettext_lazy as _
from django_bleach.models import BleachField
from django_common_utils.libraries.handlers import HandlerMixin, HTMLOptimizerHandler, TextOptimizerHandler
from django_common_utils.libraries.models import RandomIDMixin
from django_common_utils.libraries.models.mixins.date import EditCreationDateMixin

from apps.authentication.public import *
from constants import maxlength


class News(RandomIDMixin, HandlerMixin, EditCreationDateMixin):
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
