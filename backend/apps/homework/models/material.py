from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin

from apps.lesson.public import *
from apps.utils.models import AddedAtMixin


# TODO: Add multiple databases!
class Material(RandomIDMixin, AddedAtMixin):
    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materialien")
        ordering = ("-added_at", "name")
    
    lesson = models.ForeignKey(
        LESSON,
        verbose_name=lesson_single,
        on_delete=models.CASCADE,
    )
    
    # TODO: Add secure file detection!
    file = models.FileField(
        verbose_name=_("Datei"),
        blank=True,
        null=True
    )
    
    name = models.CharField(
        verbose_name=_("Dateiname"),
        max_length=255,
    )
    
    def __str__(self):
        return f"{self.name}"
