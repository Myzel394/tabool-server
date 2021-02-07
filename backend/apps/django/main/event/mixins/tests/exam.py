from datetime import date, timedelta

import lorem

from apps.django.main.event.models import Exam
from apps.django.main.timetable.mixins import joinkwargs, LessonTestMixin

__all__ = [
    "ExamTestMixin"
]


class ExamTestMixin(LessonTestMixin):
    @classmethod
    def Create_exam(cls, **kwargs) -> Exam:
        return Exam.objects.create(
            **joinkwargs({
                "course": cls.Create_course,
                "title": lambda: lorem.text().split(" ")[0],
                "information": lorem.paragraph,
                "date": lambda: date.today() + timedelta(days=5)
            }, kwargs)
        )
