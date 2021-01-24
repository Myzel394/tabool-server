from apps.django.main.lesson.mixins.tests import LessonTestMixin
from apps.django.main.lesson.models import LessonAbsence
from apps.django.utils.tests import joinkwargs


class LessonAbsenceTestMixin(LessonTestMixin):
    @classmethod
    def Create_lesson_absence(cls, **kwargs) -> LessonAbsence:
        return LessonAbsence.objects.create(
            **joinkwargs(
                {
                    "lesson": cls.Create_lesson,
                    "associated_user": lambda: cls.associated_user
                },
                kwargs
            )
        )
