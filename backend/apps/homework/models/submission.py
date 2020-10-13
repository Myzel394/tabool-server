from pathlib import Path
from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import CreationDateMixin, RandomIDMixin
from django_lifecycle import AFTER_DELETE, BEFORE_UPDATE, hook, LifecycleModel

from apps.lesson.public import *
from ..exceptions import *
from ..public import build_submission_upload_to
from ..querysets import SubmissionQuerySet
from ...utils import AssociatedUserMixin
from ...utils.fields import SafeFileField

if TYPE_CHECKING:
    from datetime import datetime
    from apps.lesson.models import Lesson

__all__ = [
    "Submission"
]


class Submission(RandomIDMixin, AssociatedUserMixin, CreationDateMixin, LifecycleModel):
    class Meta:
        verbose_name = _("Einreichung")
        verbose_name_plural = _("Einreichungen")
        ordering = ("lesson", "upload_at")
    
    objects = SubmissionQuerySet.as_manager()
    
    lesson = models.ForeignKey(
        LESSON,
        verbose_name=lesson_single,
        on_delete=models.CASCADE,
    )  # type: Lesson
    
    # TODO: Create SafeFileField!
    file = SafeFileField(
        verbose_name=_("Datei"),
        upload_to=build_submission_upload_to,
        max_length=1023
    )  # type: SafeFileField
    
    upload_at = models.DateTimeField(
        verbose_name=_("Hochladedatum"),
        help_text=_("Wann soll die Datei hochgeladen werden?"),
        blank=True,
        null=True
    )  # type: datetime
    
    is_uploaded = models.BooleanField(
        verbose_name=_("Hochgeladen?"),
        default=False
    )  # type: bool
    
    is_uploading = models.BooleanField(
        verbose_name=_("Wird hochgeladen"),
        help_text=_("Wenn ja, dann versucht der Server gerade die Datei hochzuladen."),
        default=False
    )  # type: bool
    
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
