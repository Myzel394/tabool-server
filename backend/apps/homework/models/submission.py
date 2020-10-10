from pathlib import Path

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import CreationDateMixin, RandomIDMixin
from django_lifecycle import AFTER_DELETE, BEFORE_UPDATE, hook, LifecycleModel

from apps.authentication.public import *
from apps.lesson.public import *
from ..exceptions import *

__all__ = [
    "Submission"
]


class Submission(RandomIDMixin, CreationDateMixin, LifecycleModel):
    class Meta:
        verbose_name = _("Einreichung")
        verbose_name_plural = _("Einreichungen")
        ordering = ("lesson", "upload_at")
    
    user = models.ForeignKey(
        USER,
        verbose_name=user_single,
        on_delete=models.CASCADE,
    )
    
    lesson = models.ForeignKey(
        LESSON,
        verbose_name=lesson_single,
        on_delete=models.CASCADE,
    )
    
    # TODO: Create SafeFileField!
    file = models.FileField(
        verbose_name=_("Datei")
    )
    
    upload_at = models.DateTimeField(
        verbose_name=_("Hochladedatum"),
        help_text=_("Wann soll die Datei hochgeladen werden?"),
        blank=True,
        null=True
    )
    
    is_uploaded = models.BooleanField(
        verbose_name=_("Hochgeladen?"),
        default=False
    )
    
    is_uploading = models.BooleanField(
        verbose_name=_("Wird hochgeladen"),
        help_text=_("Wenn ja, dann versucht der Server die Datei gerade hochzuladen."),
        default=False
    )
    
    @hook(BEFORE_UPDATE)
    def _hook_validate_upload_at_not_already_uploaded(self):
        if self.is_uploaded and self.has_changed("upload_at"):
            raise FileAlreadyUploadedError(_(
                "Die Datei wurde bereits am {upload_date} hochgeladen. Das Hochladedatum kann daher nicht mehr "
                "geändert werden."
            ), self.upload_at)
    
    @hook(AFTER_DELETE)
    def _hook_delete_file(self):
        Path(self.file.path).unlink(missing_ok=True)
    
    def __str__(self):
        # Translators: Diese Nachricht ist für den Admin-Bereich. Sie wird verwendet, um Einreichungen darzustellen.
        return _("{filename} für Stunde {lesson} (Hochladedatum: {upload_date})").format(
            filename=self.file.name,
            lesson=self.lesson,
            upload_date=self.upload_at
        )
