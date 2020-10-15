from datetime import date

from apps.scooso_scraper.scrapers.timetable import TimetableRequest
from apps.utils import UserTestMixin


class FullTest(UserTestMixin):
    def setUp(self) -> None:
        self.load_dummy_user()
        self.logged_user = self.Create_user()
        self.__class__.associated_user = self.logged_user
    
    def test_timetable(self):
        test = True
        
        # TODO: Add!
        if test:
            scraper = TimetableRequest(self.username, self.password)
            timetable = scraper.get_timetable(date(2020, 10, 5), date(2020, 10, 9))
