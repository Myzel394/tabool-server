from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin

from apps.event.options import ModificationTypeOptions
from apps.event.sub.subquerysets.modification import ModificationQuerySet
from apps.lesson.public import *

__all__ = [
    "Modification"
]


class Modification(RandomIDMixin):
    class Meta:
        verbose_name = _("Veränderung")
        verbose_name_plural = _("Veränderungen")
        ordering = ("start_datetime",)
    
    objects = ModificationQuerySet.as_manager()
    
    course = models.ForeignKey(
        COURSE,
        verbose_name=course_single,
        on_delete=models.CASCADE,
    )
    
    new_room = models.ForeignKey(
        ROOM,
        verbose_name=room_single,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    
    new_teacher = models.ForeignKey(
        TEACHER,
        verbose_name=teacher_single,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    
    new_subject = models.ForeignKey(
        SUBJECT,
        verbose_name=subject_single,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    
    start_datetime = models.DateTimeField(
        verbose_name=_("Start"),
    )
    
    end_datetime = models.DateTimeField(
        verbose_name=_("Ende")
    )
    
    information = models.TextField(
        verbose_name=_("Information"),
        blank=True,
        null=True
    )
    
    modification_type = models.PositiveSmallIntegerField(
        choices=ModificationTypeOptions.choices,
        verbose_name=_("Typ"),
        help_text=_("Art von Veränderung")
    )
