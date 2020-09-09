from typing import *

from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .models import Lesson

def validate_lessons_dont_overlap(lessons: QueryType[Lesson]):
    """Validates whether there are no overlapping lessons"""
    for lesson in lessons:
        if lesson.filter(
            weekday=lesson.weekday,
            Q(
                start_time__gt=lesson.start_time,
                start_time__lt=lesson.end_time
            ) |
            Q(
                end_time__gt=lesson.start_time,
                end_time__lt=lesson.end_time
            )
        ).exists():
            raise ValidationError(
                _("{} dürfen sich nicht überlappen!".format(model_verbose_plural(Lesson)))
            )
          