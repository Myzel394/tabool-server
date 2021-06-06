from datetime import datetime, timedelta

from django.core.exceptions import ValidationError

from apps.django.main.homework.mixins import MaterialTestMixin
from apps.django.main.homework.models import Material
from apps.django.utils.tests_mixins import GenericAPITestMixin


class MaterialModelTest(MaterialTestMixin):
    def test_date_must_be_in_future(self):
        with self.assertRaises(ValidationError):
            self.Create_material(
                publish_datetime=datetime.now() - timedelta(days=5)
            )

    def test_autofill_name(self):
        material = self.Create_material(
            name=None
        )
        self.assertIsNotNone(material.name)


class StudentMaterialAPITest(MaterialTestMixin, GenericAPITestMixin):
    def setUp(self):
        self.__class__.associated_student = self.Login_student()

    def test_can_access(self):
        self.generic_access_test(
            obj=self.Create_material(),
            api_suffix="student/"
        )

    def test_can_not_do_lifecycle_methods(self):
        self.generic_lifecycle_test(
            model=Material,
            post_data={},
            patch_data={},
            api_suffix="student/",
            should_be_ok=False,
            foreign_obj=self.Create_material()
        )


class TeacherMaterialAPITest(MaterialTestMixin):
    def setUp(self):
        self.teacher = self.Login_teacher()
        self.__class__.associated_teacher = self.teacher

    def test_can_not_change_announce_when_already_true(self):
        material = self.Create_material(
            announce=True
        )
        response = self.client.patch(f"/api/teacher/material/{material.id}/", {
            "announce": False
        }, content_type="application/json")
        self.assertEqual(400, response.status_code)
