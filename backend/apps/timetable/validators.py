from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.utils import model_verbose_plural
from django_hint import QueryType

from apps.subject.models import LessonData


def validate_lessons_dont_overlap(lessons: QueryType[LessonData]):
    """Validates whether there are no overlapping lessons"""
    for lesson in lessons:
        if LessonData.objects.filter(
                Q(
                    start_time__gt=lesson.start_time,
                    start_time__lt=lesson.end_time
                ) |
                Q(
                    end_time__gt=lesson.start_time,
                    end_time__lt=lesson.end_time
                ),
                weekday=lesson.weekday,
        ).exists():
            raise ValidationError(
                _("{} dürfen sich nicht überlappen!").format(model_verbose_plural(LessonData))
            )
