from pathlib import Path
from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_lifecycle import AFTER_DELETE, BEFORE_UPDATE, hook, LifecycleModel

from apps.lesson.public import *
from apps.utils.models import AddedAtMixin, model_verbose
from ..public import *
from ..querysets import MaterialQuerySet
from ...utils.fields import SafeFileField

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
    
    file = SafeFileField(
        verbose_name=_("Datei"),
        blank=True,
        null=True,
        upload_to=build_material_upload_to,
        max_length=1023
    )  # type: SafeFileField
    
    name = models.CharField(
        verbose_name=_("Dateiname"),
        max_length=255,
        blank=True,
        null=True
    )  # type: str
    
    def __str__(self):
        return _("{material_model_verbose} {name} für {lesson}").format(
            material_model_verbose=model_verbose(self),
            name=self.name,
            lesson=self.lesson
        )
    
    @hook(AFTER_DELETE)
    def _hook_delete_file(self):
        Path(self.file.path).unlink(missing_ok=True)
    
    @hook(BEFORE_UPDATE, when_any=["name", "file"])
    def _hook_validate_name_and_file(self):
        if self.file is not None and self.name is None:
            raise ValueError(_("Dateiname fehlt!"))
    
    @property
    def folder_name(self) -> str:
        return f"{self.lesson.lesson_data.course.folder_name}/{self.id}"
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
