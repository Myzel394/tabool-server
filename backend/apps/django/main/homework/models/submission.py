from pathlib import Path
from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import CreationDateMixin, RandomIDMixin
from django_lifecycle import BEFORE_DELETE, BEFORE_SAVE, hook, LifecycleModel
from private_storage.fields import PrivateFileField

from apps.django.authentication.user.public import *
from apps.django.authentication.user.public import model_names as auth_names
from ..file_uploads import build_submission_upload_to
from ..public import model_names
from ..sub.subquerysets.submission import SubmissionQuerySet
from ...timetable.mixins import LessonMixin

if TYPE_CHECKING:
    from apps.django.authentication.user.models import User, Student
    from django.db.models.fields.files import FieldFile

__all__ = [
    "Submission"
]


class Submission(RandomIDMixin, LessonMixin, LifecycleModel, CreationDateMixin):
    class Meta:
        verbose_name = model_names.SUBMISSION
        verbose_name_plural = model_names.SUBMISSION_PLURAL
        ordering = ("name", "publish_datetime", "-created_at")

    objects = SubmissionQuerySet.as_manager()

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=31,
        blank=True,
    )

    file = PrivateFileField(
        verbose_name=_("Datei"),
        upload_to=build_submission_upload_to,
        max_length=1023,
    )  # type: FieldFile

    publish_datetime = models.DateTimeField(
        verbose_name=_("Veröffentlichkeitsdatum"),
        help_text=_("Ab wann die Datei für den Lehrer sichtbar ist."),
        null=True,
        blank=True,
    )

    student = models.ForeignKey(
        STUDENT,
        verbose_name=auth_names.STUDENT,
        on_delete=models.CASCADE,
    )  # type: Student

    def can_user_access_file(self, user: "User") -> bool:
        if user.is_student:
            return self.student == user.student
        return self.lesson.course.teacher == user.teacher

    @property
    def folder_name(self) -> str:
        return f"{self.lesson.course.folder_name}"

    @hook(BEFORE_DELETE)
    def _hook_delete_file(self):
        Path(self.file.path).unlink(missing_ok=True)

    @hook(BEFORE_SAVE)
    def _hook_full_clean(self):
        self.full_clean()

    @hook(BEFORE_SAVE)
    def _hook_autofill_name(self):
        if not self.name or self.name == "":
            self.name = Path(self.file.path).name
