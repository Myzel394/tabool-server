from datetime import datetime, timedelta

import lorem

from apps.django.main.event.models import Event
from apps.django.main.timetable.mixins import joinkwargs, LessonTestMixin

__all__ = [
    "EventTestMixin"
]


class EventTestMixin(LessonTestMixin):
    @classmethod
    def Create_event(cls, **kwargs) -> Event:
        lesson = kwargs.pop("lesson", None) or cls.Create_lesson()
        
        return Event.objects.create(
            **joinkwargs({
                **cls.Create_lesson_argument(lesson, kwargs.pop("lesson_date", None)),
                "title": lorem.text,
                "start_datetime": lambda: datetime.now() + timedelta(days=1),
                "end_datetime": lambda: datetime.now() + timedelta(days=1, hours=1),
            }, kwargs)
        )
