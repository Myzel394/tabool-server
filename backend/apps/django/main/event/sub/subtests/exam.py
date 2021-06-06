from datetime import date, timedelta

from apps.django.main.event.mixins import ExamTestMixin
from apps.django.main.event.models import Exam
from apps.django.utils.tests_mixins import GenericAPITestMixin


class StudentExamAPITest(ExamTestMixin, GenericAPITestMixin):
    def setUp(self):
        self.__class__.associated_student = self.Login_student()

    def test_access(self):
        self.generic_access_test(
            obj=self.Create_exam(),
            api_suffix="student/",
        )

    def test_lifecycle(self):
        self.generic_lifecycle_test(
            model=Exam,
            post_data={
                "course": self.Create_course().id,
                "title": "Title",
                "date": date.today() + timedelta(days=5)
            },
            patch_data={
                "information": "Test"
            },
            api_suffix="student/",
            should_be_ok=False,
            foreign_obj=self.Create_exam()
        )


class TeacherExamAPITest(ExamTestMixin, GenericAPITestMixin):
    def setUp(self):
        self.__class__.associated_teacher = self.Login_teacher()

    def test_generic(self):
        self.generic_elements_test(
            model=Exam,
            post_data={
                "course": self.Create_course().id,
                "title": "Title",
                "date": date.today() + timedelta(days=5),
                "information": "Information"
            },
            patch_data={
                "information": "Test"
            },
            api_suffix="teacher/"
        )
