import random
from datetime import date, datetime, time, timedelta
from typing import *

from dateutil.rrule import MINUTELY, rrule

from apps.django.main.school_data.mixins.tests import *
from apps.django.utils.tests import *
from apps.utils import find_next_date_by_weekday
from apps.utils.time import dummy_datetime_from_target
from constants.weekdays import ALLOWED_WEEKDAYS
from .course import CourseTestMixin
from ...models import Lesson, LessonData

__all__ = [
    "LessonTestMixin"
]


class LessonTestMixin(
    RoomTestMixin,
    StartTimeEndTimeTestMixin,
    CourseTestMixin
):
    @classmethod
    def Create_lesson(cls, **kwargs) -> Lesson:
        lesson_data = kwargs.pop("lesson_data", cls.Create_lesson_data())
        
        return Lesson.objects.create(
            **joinkwargs(
                {
                    "date": lambda: find_next_date_by_weekday(date.today(), lesson_data.weekday),
                    "lesson_data": lambda: lesson_data,
                },
                kwargs
            )
        )
    
    @classmethod
    def Create_lesson_data(cls, **kwargs) -> LessonData:
        return LessonData.objects.create(
            **joinkwargs(
                {
                    "room": cls.Create_room,
                    "course": cls.Create_course,
                    "start_time": cls.start_time,
                    "end_time": cls.end_time,
                    "weekday": lambda: random.choice([x[0] for x in ALLOWED_WEEKDAYS]),
                },
                kwargs
            )
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
        end_time = end_time or (
                dummy_datetime_from_target(time(hour=13, minute=10)) - timedelta(minutes=duration)).time()
        
        lessons = []
        
        weekday: int
        for weekday in [x[0] for x in ALLOWED_WEEKDAYS]:
            current_time: datetime
            for current_time in rrule(
                    MINUTELY,
                    interval=duration,
                    dtstart=dummy_datetime_from_target(start_time),
                    until=dummy_datetime_from_target(end_time)
            ):
                lesson = cls.Create_lesson_data(
                    **joinkwargs(
                        {
                            "start_time": lambda: current_time.time(),
                            "end_time": lambda: (current_time + timedelta(minutes=duration)).time(),
                            "weekday": lambda: weekday,
                        },
                        kwargs
                    )
                )
                lessons.append(lesson)
        
        return lessons


"""
class LessonUploadTestMixin(LessonTestMixin, DummyUser):
    def load_lesson_upload(self):
        self.logged_user = self.Login_user()
        self.__class__.associated_user = self.logged_user
        self.load_dummy_user()
        
        self.time_id = int(os.getenv("LESSON_ID"))
        self.target_date = datetime.strptime(os.getenv("DATE"), "%Y.%m.%d.%H.%M.%S")
        
        self.lesson = self.Create_lesson(
            date=self.target_date
        )
        scooso_data = LessonScoosoData.objects.create(
            lesson=self.lesson,
            time_id=self.time_id
        )
"""
