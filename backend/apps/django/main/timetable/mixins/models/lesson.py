import calendar
from typing import *

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from ...models import Lesson
from ...public import *
from ...public import model_names

__all__ = [
    "LessonMixin"
]


def validate_lesson(instance: "LessonMixin"):
    if instance.USER_FIELD:
        qs = Lesson.objects.from_user(getattr(instance, instance.USER_FIELD))
    else:
        qs = Lesson.objects.all()
    
    # Validate access
    if instance.lesson not in qs:
        raise ValidationError(
            _("Du hast keinen Zugriff auf diese Unterrichtsstunde.")
        )
    
    # Validate date
    valid_weekday = instance.lesson.weekday
    if instance.lesson_date.weekday() != valid_weekday:
        weekday_names = list(calendar.day_name)
        
        raise ValidationError({
            "lesson_date": _("Das Datum für diesen Tag ist nicht gültig, es muss ein {weekday} sein.").format(
                weekday=weekday_names[valid_weekday]
            )})


class LessonMixin(LifecycleModel):
    class Meta:
        abstract = True
    
    USER_FIELD: Optional[str] = None
    
    lesson = models.ForeignKey(
        LESSON,
        verbose_name=model_names.LESSON,
        on_delete=models.CASCADE,
    )  # type: Lesson
    
    lesson_date = models.DateField(
        verbose_name=_("Datum"),
    )
    
    def clean(self):
        validate_lesson(self)
        
        return super().clean()
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when_any=["lesson", "lesson_date"], has_changed=True)
    def _hook_full_clean(self):
        self.full_clean()
