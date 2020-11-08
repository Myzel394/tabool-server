from datetime import date

from apps.django.extra.scooso_scraper.scrapers.timetable import TimetableRequest
from apps.django.utils.tests import DummyUser, UserTestMixin


class SomeTests(UserTestMixin, DummyUser):
    def setUp(self) -> None:
        self.load_dummy_user()
    
    def test_month(self):
        with TimetableRequest(self.username, self.password) as scraper:
            data = scraper.get_timetable(date(2020, 11, 2), date(2020, 11, 6))
        
        print(data)
