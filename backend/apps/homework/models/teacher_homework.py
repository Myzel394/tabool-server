from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.subject.models import Teacher
from .mixins.homework import BaseHomeworkMixin
from ..querysets import TeacherHomeworkQuerySet

__all__ = [
    "TeacherHomework"
]


class TeacherHomework(BaseHomeworkMixin):
    class Meta:
        verbose_name = _("Lehrer-Hausaufgabe")
        verbose_name_plural = _("Lehrer-Hausaufgaben")
        ordering = ("-completed", "due_date")
    
    objects = TeacherHomeworkQuerySet.as_manager()
    
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


"""
class Submission(RandomIDMixin, AssociatedUserMixin, DatesMixin):
    class Meta:
        verbose_name = _("Einreichung")
        verbose_name_plural = _("Einreichungen")
        ordering = ("-last_edited_at", "-created_at")

    homework = models.ForeignKey(
        Homework,
        verbose_name=model_verbose(Homework),
        on_delete=models.CASCADE,
    )

    files = models.ManyToManyField(
        "SubmissionFile",
        verbose_name=model_verbose_plural("SubmissionFile"),
    )


class SubmissionFile(RandomIDMixin, AssociatedUserMixin, DatesMixin):
    class Meta:
        verbose_name = _("Datei-Einreichung")
        verbose_name_plural = _("Datei-Einreichungen")
        ordering = ("-last_edited_at", "-created_at")

    file = models.FileField(
        verbose_name=_("Datei"),
    )

    name = models.CharField(
        verbose_name=_("Dateienname")
    )"""
