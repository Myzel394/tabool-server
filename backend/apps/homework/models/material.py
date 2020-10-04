from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import CreationDateMixin, RandomIDMixin
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel
from private_storage.fields import PrivateFileField
from secure_file_detection.constants import SUPPORTED_MIMETYPES

from apps.lesson.public import *
from .. import constants
from ..helpers import build_material_path, validate_material_file
from ..querysets import MaterialQuerySet

if TYPE_CHECKING:
    from apps.lesson.models import Lesson
    from django.db.models.fields.files import FieldFile

__all__ = [
    "Material"
]


class Material(RandomIDMixin, CreationDateMixin, LifecycleModel):
    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materialien")
        ordering = ("lesson", "created_at")
    
    objects = MaterialQuerySet.as_manager()
    
    lesson = models.ForeignKey(
        LESSON,
        verbose_name=lesson_single,
        on_delete=models.CASCADE,
    )  # type: Lesson
    
    file = PrivateFileField(
        verbose_name=_("Datei"),
        upload_to=build_material_path,
        content_types=SUPPORTED_MIMETYPES,
        max_file_size=constants.MAX_UPLOAD_SIZE,
    )  # type: FieldFile
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="file")
    def _hook_validate_file(self):
        data = self.file.read()
        
        validate_material_file(data)
