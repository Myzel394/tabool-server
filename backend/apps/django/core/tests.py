import os
from datetime import datetime

import lorem

from apps.django.extra.scooso_scraper.scrapers.timetable import TimetableRequest
from apps.django.main.homework.mixins.tests import HomeworkTestMixin
from apps.django.utils.tests import *
from constants.api import API_VERSION


class FullTest(UserTestMixin):
    def setUp(self) -> None:
        self.load_dummy_user()
        self.logged_user = self.Create_user()
        self.__class__.associated_user = self.logged_user
        self.start_date = datetime.strptime(os.getenv("DATA_START_DATE"), os.getenv("DATE_FORMAT")).date()
        self.end_date = datetime.strptime(os.getenv("DATA_END_DATE"), os.getenv("DATE_FORMAT")).date()
    
    def test_timetable(self):
        test = True
        
        if test:
            scraper = TimetableRequest(self.username, self.password)
            timetable = scraper.get_timetable(self.start_date, self.end_date)
            scraper.import_timetable_from_scraper(timetable)


class LargeUserTest(HomeworkTestMixin):
    def setUp(self) -> None:
        self.test = False
    
    def test_large_user_time_needed(self):
        if self.test:
            times = []
            
            for i in range(50):
                with self.Login_user_as_context() as _:
                    print("Creating user no.", i)
                    lesson = self.Create_lesson()
                    homework = self.Create_homework()
                    homework.delete()
                    
                    start_time = datetime.now()
                    self.client.post(
                        f"/api/{API_VERSION}/data/homework/",
                        {
                            "lesson": lesson.id,
                            "information": lorem.text() * 4
                        },
                        content_type="application/json"
                    )
                    diff = datetime.now() - start_time
                
                times.append(diff)
            
            print("Evaluating times")
            elapsed_micro = [
                time.microseconds
                for time in times
            ]
            
            average = sum(elapsed_micro) / len(elapsed_micro)
            best = min(elapsed_micro)
            worst = max(elapsed_micro)
            print("Average time:", average / 1000, "milliseconds")
            print("Best time:", best / 1000, "milliseconds")
            print("Worst time:", worst / 1000, "milliseconds")
