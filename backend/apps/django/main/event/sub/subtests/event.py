from datetime import datetime, timedelta

from apps.django.main.event.mixins import EventTestMixin
from apps.django.main.event.models import Event
from apps.django.utils.tests_mixins import GenericAPITestMixin


class StudentEventAPITest(EventTestMixin, GenericAPITestMixin):
    def setUp(self):
        self.__class__.associated_student = self.Login_student()

    def test_access(self):
        self.generic_access_test(
            obj=self.Create_event(),
            api_suffix="student/",
        )

    def test_lifecycle(self):
        self.generic_lifecycle_test(
            model=Event,
            post_data={
                "title": "Title",
                "start_datetime": datetime.now(),
                "end_datetime": datetime.now() + timedelta(days=1)
            },
            patch_data={
                "title": "Test"
            },
            api_suffix="student/",
            should_be_ok=False,
            foreign_obj=self.Create_event()
        )


class TeacherEventAPITest(EventTestMixin, GenericAPITestMixin):
    def setUp(self):
        self.__class__.associated_teacher = self.Login_teacher()

    def test_access(self):
        self.generic_access_test(
            obj=self.Create_event(),
            api_suffix="teacher/",
        )
