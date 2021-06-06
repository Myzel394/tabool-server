import random

import lorem

from apps.django.main.event.models import Modification
from apps.django.main.event.options import ModificationTypeOptions
from apps.django.main.timetable.mixins import joinkwargs, LessonTestMixin

__all__ = [
    "ModificationTestMixin"
]


class ModificationTestMixin(LessonTestMixin):
    @classmethod
    def Create_modification(cls, **kwargs) -> Modification:
        lesson = kwargs.pop("lesson", None) or cls.Create_lesson()

        return Modification.objects.create(
            **joinkwargs({
                **cls.Create_lesson_argument(lesson, kwargs.pop("lesson_date", None)),
                "information": lorem.paragraph,
                "new_room": cls.Create_room,
                "new_subject": cls.Create_subject,
                "new_teacher": cls.Create_teacher,
                "modification_type": lambda: random.choice(ModificationTypeOptions.values)
            }, kwargs)
        )
