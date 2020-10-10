from pathlib import Path
from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_lifecycle import AFTER_DELETE, BEFORE_UPDATE, hook, LifecycleModel

from apps.lesson.public import *
from apps.utils.models import AddedAtMixin
from ..public import *
from ..querysets import MaterialQuerySet

if TYPE_CHECKING:
    from apps.lesson.models import Lesson


# TODO: Add multiple databases!
class Material(RandomIDMixin, AddedAtMixin, LifecycleModel):
    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materialien")
        ordering = ("-added_at", "name")
    
    objects = MaterialQuerySet.as_manager()
    
    lesson = models.ForeignKey(
        LESSON,
        verbose_name=lesson_single,
        on_delete=models.CASCADE,
    )  # type: Lesson
    
    # TODO: Add secure file detection!
    file = models.FileField(
        verbose_name=_("Datei"),
        blank=True,
        null=True,
        upload_to=build_material_upload_to
    )
    
    name = models.CharField(
        verbose_name=_("Dateiname"),
        max_length=255,
        blank=True,
        null=True
    )  # type: str
    
    def __str__(self):
        return f"{self.name}"
    
    @hook(AFTER_DELETE)
    def _hook_delete_file(self):
        Path(self.file.path).unlink(missing_ok=True)
    
    @hook(BEFORE_UPDATE, when_any=["name", "file"])
    def _hook_validate_name_and_file(self):
        if self.file is not None and self.name is None:
            raise ValueError(_("Dateiname fehlt!"))
    
    @property
    def folder_name(self) -> str:
        return self.lesson.lesson_data.course.name
