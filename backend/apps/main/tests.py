import os
from datetime import datetime

from apps.scooso_scraper.scrapers.timetable import TimetableRequest
from apps.utils import UserTestMixin


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
