import lorem

from apps.django.main.homework.models import Classbook
from apps.django.main.timetable.mixins import joinkwargs, LessonTestMixin

__all__ = [
    "ClassbookTestMixin"
]


class ClassbookTestMixin(LessonTestMixin):
    @classmethod
    def Create_classbook(cls, **kwargs) -> Classbook:
        lesson = kwargs.pop("lesson", None) or cls.Create_lesson()

        return Classbook.objects.create(
            **joinkwargs({
                "presence_content": lorem.paragraph,
                "online_content": lorem.paragraph,
                **cls.Create_lesson_argument(lesson, kwargs.pop("lesson_date", None))
            }, kwargs)
        )
