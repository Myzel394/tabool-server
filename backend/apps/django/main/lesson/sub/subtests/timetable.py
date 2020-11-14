import json
import os
from datetime import datetime
from pprint import pp

from apps.django.extra.scooso_scraper.actions import fetch_timetable
from apps.django.main.event.mixins.tests import ModificationTestMixin
from apps.django.main.lesson.mixins.tests import LessonTestMixin
from apps.django.main.lesson.models import Lesson
from apps.django.utils.tests import ClientTestMixin, DummyUser, UserTestMixin


class TimetableAPITest(LessonTestMixin, ModificationTestMixin, ClientTestMixin, UserTestMixin, DummyUser):
    def setUp(self) -> None:
        self.load_dummy_user()
        self.__class__.associated_user = self.Login_user()
        
        start_datetime = datetime.strptime(os.getenv("DATA_START_DATE"), os.getenv("DATE_FORMAT"))
        end_datetime = datetime.strptime(os.getenv("DATA_END_DATE"), os.getenv("DATE_FORMAT"))
        
        print("Fetching & importing timetable")
        fetch_timetable(self.__class__.associated_user, start_datetime, end_datetime)
        print("Done")
    
    def get_start_datetime(self) -> datetime:
        lesson = Lesson.objects.all().earliest("date")
        
        return datetime.combine(lesson.date, lesson.lesson_data.start_time)
    
    def get_end_datetime(self) -> datetime:
        lesson = Lesson.objects.all().latest("date")
        
        return datetime.combine(lesson.date, lesson.lesson_data.start_time)
    
    def test_api(self):
        response = self.client.get("/api/data/timetable/", {
            "start_datetime": self.get_start_datetime(),
            "end_datetime": self.get_end_datetime()
        }, content_type="application/json")
        
        self.assertStatusOk(response.status_code)
        
        data = json.loads(json.dumps(response.data))
        
        pp(data)
