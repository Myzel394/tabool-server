from datetime import datetime, timedelta

from user_sessions.models import Session

from apps.django.authentication.user.mixins import UserTestMixin


class SessionsTest(UserTestMixin):
    def setUp(self):
        self.user = self.Create_user()

    def test_session_creates(self):
        session = Session.objects.create(
            user=self.user,
            expire_date=datetime.now() + timedelta(days=10)
        )

        # Ensure raises no error
        print(session.sessionrelation)
