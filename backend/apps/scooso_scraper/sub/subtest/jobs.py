from apps.scooso_scraper.cron_jobs import fetch_timetable_from_users
from apps.utils import UserTestMixin


class JobTest(UserTestMixin):
    def test_fetch_timetable(self):
        print("Creating users")
        for _ in range(0):
            self.Create_user()
        
        with self.Login_user_as_context() as user:
            print("Fetching data")
            fetch_timetable_from_users()
