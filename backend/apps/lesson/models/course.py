from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models import RandomIDMixin

from ..public import model_references, model_verbose_functions
from ..querysets import CourseQuerySet


__all__ = [
    "Course"
]


class Course(RandomIDMixin):
    class Meta:
        verbose_name = _("Kurs")
        verbose_name_plural = _("Kurse")
    
    objects = CourseQuerySet.as_manager()
    
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Teilnehmer"),
    )
    
    subject = models.ForeignKey(
        model_references.SUBJECT,
        verbose_name=model_verbose_functions.subject_single,
        on_delete=models.CASCADE,
    )
    
    teacher = models.ForeignKey(
        model_references.TEACHER,
        verbose_name=model_verbose_functions.teacher_single,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    
    name = models.CharField(
        verbose_name=_("Name"),
        blank=True,
        null=True,
        max_length=7
    )
