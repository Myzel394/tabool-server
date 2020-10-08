from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_lifecycle import BEFORE_UPDATE, hook

from apps.authentication.public import model_references
from apps.utils.models import AddedAtMixin


# TODO: Add multiple databases!
class Material(RandomIDMixin, AddedAtMixin):
    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materialien")
        ordering = ("-added_at", "name")
    
    # TODO: Add secure file detection!
    file = models.FileField(
        verbose_name=_("Datei"),
    )
    
    name = models.CharField(
        verbose_name=_("Dateiname"),
        max_length=255,
    )
