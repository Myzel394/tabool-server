import os
from datetime import datetime

from apps.django.extra.scooso_scraper.actions import fetch_timetable
from apps.django.extra.scooso_scraper.mixins.tests import DummyUser
from apps.django.main.event.mixins.tests import ClientTestMixin, ModificationTestMixin, UserTestMixin
from apps.django.main.lesson.mixins.tests import LessonTestMixin
from apps.django.main.lesson.models import Lesson


class TimetableAPITest(LessonTestMixin, ModificationTestMixin, ClientTestMixin, UserTestMixin, DummyUser):
    def setUp(self) -> None:
        if os.getenv("GITHUB_WORKFLOW"):
            return None
    
    def get_start_datetime(self) -> datetime:
        if Lesson.objects.count() == 0:
            return datetime(2020, 1, 1)
        
        lesson = Lesson.objects.all().earliest("date")
        
        return datetime.combine(lesson.date, lesson.start_time)
    
    def get_end_datetime(self) -> datetime:
        if Lesson.objects.count() == 0:
            return datetime(2020, 1, 2)
        
        lesson = Lesson.objects.all().latest("date")
        
        return datetime.combine(lesson.date, lesson.start_time)
    
    def test_fetch_timetable(self):
        if os.getenv("GITHUB_WORKFLOW"):
            return None
        
        self.load_dummy_user()
        user = self.Login_user()
        
        start_datetime = datetime.strptime(os.getenv("DATA_START_DATE"), os.getenv("DATE_FORMAT"))
        end_datetime = datetime.strptime(os.getenv("DATA_END_DATE"), os.getenv("DATE_FORMAT"))
        
        fetch_timetable(user, start_datetime, end_datetime, in_thread=False)
        
        response = self.client.get("/api/data/timetable/", {
            "start_datetime": self.get_start_datetime(),
            "end_datetime": self.get_end_datetime()
        }, content_type="application/json")
        
        self.assertStatusOk(response.status_code)
    
    def test_fetch_timetable_not_available(self):
        self.Login_user()
        
        response = self.client.get("/api/data/timetable/", {
            "start_datetime": self.get_start_datetime(),
            "end_datetime": self.get_end_datetime()
        }, content_type="application/json")
        
        self.assertEqual(503, response.status_code)
