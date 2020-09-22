import random
from datetime import datetime, time, timedelta
from typing import *

from dateutil.rrule import MINUTELY, rrule

from apps.utils.tests import StartTimeEndTimeTestMixin
from apps.utils.time import dummy_datetime_from_time
from .room import RoomTestMixin
from .subject import SubjectTestMixin
from .teacher import TeacherTestMixin
from ...constants import LESSON_ALLOWED_DAYS
from ...models import Lesson, LessonData

__all__ = [
    "LessonTestMixin"
]


class LessonTestMixin(
    TeacherTestMixin,
    SubjectTestMixin,
    RoomTestMixin,
    StartTimeEndTimeTestMixin
):
    @classmethod
    def Create_lesson(cls, **kwargs):
        return Lesson.objects.create_automatically(
            **{
                "lesson_data": cls.Create_lesson_data(),
                **kwargs
            }
        )
    
    @classmethod
    def Create_lesson_data(cls, **kwargs) -> LessonData:
        return LessonData.objects.create(
            **{
                "teacher": cls.Create_teacher(),
                "room": cls.Create_room(),
                "subject": cls.Create_subject(),
                "start_time": cls.start_time(),
                "end_time": cls.end_time(),
                "weekday": random.choice([x[0] for x in LESSON_ALLOWED_DAYS]),
                **kwargs
            }
        )
    
    @classmethod
    def Create_lessons_data(
            cls,
            start_time: Optional[time] = None,
            end_time: Optional[time] = None,
            duration: int = 45,
            **kwargs
    ) -> List[LessonData]:
        start_time = start_time or time(hour=7, minute=55)
        end_time = end_time or (dummy_datetime_from_time(time(hour=13, minute=10)) - timedelta(minutes=duration)).time()
        
        lessons = []
        
        weekday: int
        for weekday in [x[0] for x in LESSON_ALLOWED_DAYS]:
            current_time: datetime
            for current_time in rrule(
                    MINUTELY,
                    interval=duration,
                    dtstart=dummy_datetime_from_time(start_time),
                    until=dummy_datetime_from_time(end_time)
            ):
                lesson = cls.Create_lesson_data(
                    **{
                        "start_time": current_time.time(),
                        "end_time": (current_time + timedelta(minutes=duration)).time(),
                        "weekday": weekday,
                        **kwargs
                    }
                )
                lessons.append(lesson)
        
        return lessons
