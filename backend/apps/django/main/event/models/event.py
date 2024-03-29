from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin

from apps.django.main.course.public import *
from apps.django.main.course.public import model_names as course_names
from ..public import model_names
from ..sub.subquerysets.event import EventQuerySet

if TYPE_CHECKING:
    from apps.django.main.course.models import Room

__all__ = [
    "Event"
]


class Event(RandomIDMixin):
    class Meta:
        verbose_name = model_names.EVENT
        verbose_name_plural = model_names.EVENT_PLURAL
        ordering = ("start_datetime", "title")

    objects = EventQuerySet.as_manager()

    room = models.ForeignKey(
        ROOM,
        on_delete=models.SET_NULL,
        verbose_name=course_names.ROOM,
        blank=True,
        null=True,
    )  # type: Room

    title = models.CharField(
        verbose_name=_("Titel"),
        max_length=31,
    )

    information = models.CharField(
        blank=True,
        null=True,
        max_length=1023,
        verbose_name=_("Informationen")
    )

    start_datetime = models.DateTimeField(
        verbose_name=_("Start"),
    )

    end_datetime = models.DateTimeField(
        verbose_name=_("Ende"),
    )
