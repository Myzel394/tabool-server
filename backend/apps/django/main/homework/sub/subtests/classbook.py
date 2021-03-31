from apps.django.main.homework.mixins import ClassbookTestMixin
from apps.django.main.homework.models import Classbook
from apps.django.utils.tests_mixins import GenericAPITestMixin


class StudentClassbookAPITest(ClassbookTestMixin, GenericAPITestMixin):
    def setUp(self):
        self.student = self.Login_student()
        self.__class__.associated_student = self.student
    
    def test_access(self):
        self.generic_access_test(
            obj=self.Create_classbook(),
            api_suffix="student/"
        )
    
    def test_lifecycle(self):
        self.generic_lifecycle_test(
            model=Classbook,
            post_data=self.get_lesson_argument(),
            patch_data={
                "online_content": "Test"
            },
            api_suffix="student/",
            should_be_ok=False,
            foreign_obj=self.Create_classbook()
        )


class TeacherClassbookAPITest(ClassbookTestMixin, GenericAPITestMixin):
    def setUp(self) -> None:
        self.__class__.associated_teacher = self.Login_teacher()
    
    def test_generic(self):
        self.generic_elements_test(
            model=Classbook,
            post_data=self.get_lesson_argument(),
            patch_data={
                "online_content": "Test"
            },
            api_suffix="teacher/"
        )
