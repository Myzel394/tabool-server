from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models import CreationDateMixin, RandomIDMixin
from django_lifecycle import BEFORE_UPDATE, hook, LifecycleModel

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

    lesson = models.ForeignKey(
        LESSON,
        verbose_name=lesson_single,
        on_delete=models.CASCADE,
    )
    
    file = models.FileField(
        verbose_name=_("Datei")
    )
    
    upload_at = models.DateTimeField(
        verbose_name=_("Hochladedatum"),
        help_text=_("Wann soll die Datei hochgeladen werden?"),
        blank=True,
        null=True
    )
    
    uploaded = models.BooleanField(
        verbose_name=_("Hochgeladen?"),
        default=False
    )
    
    @hook(BEFORE_UPDATE)
    def _hook_validate_upload_at_not_already_uploaded(self):
        if self.uploaded and self.has_changed(self.upload_at):
            raise FileAlreadyUploadedError(_(
                "Die Datei wurde beeits hochgeladen. Das Hochladedatum kann daher nicht geändert werden.n"
            ))
    
    

