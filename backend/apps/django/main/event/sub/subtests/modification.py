import random

from apps.django.main.event.mixins import ModificationTestMixin
from apps.django.main.event.models import Modification
from apps.django.main.event.options import ModificationTypeOptions
from apps.django.utils.tests_mixins import GenericAPITestMixin


class StudentModificationAPITest(ModificationTestMixin, GenericAPITestMixin):
    def setUp(self):
        self.student = self.Login_student()
        self.__class__.associated_student = self.student

    def test_access(self):
        self.generic_access_test(
            obj=self.Create_modification(),
            api_suffix="student/",
        )

    def test_lifecycle(self):
        self.generic_lifecycle_test(
            model=Modification,
            post_data=self.get_lesson_argument(),
            patch_data={
                "information": "Test"
            },
            api_suffix="student/",
            should_be_ok=False,
            foreign_obj=self.Create_modification()
        )


class TeacherModificationAPITest(ModificationTestMixin, GenericAPITestMixin):
    def setUp(self):
        self.teacher = self.Login_teacher()
        self.__class__.associated_teacher = self.teacher

    def test_generic(self):
        self.generic_elements_test(
            model=Modification,
            post_data={
                **self.get_lesson_argument(),
                "modification_type": random.choice(ModificationTypeOptions.values)  # nosec
            },
            patch_data={
                "information": "Test"
            },
            api_suffix="teacher/"
        )
