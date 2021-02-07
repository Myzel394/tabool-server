from datetime import datetime, timedelta

from django.core.exceptions import ValidationError

from apps.django.main.homework.mixins import MaterialTestMixin


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


class MaterialAPITest(MaterialTestMixin):
    def setUp(self):
        self.teacher = self.Login_teacher()
        self.__class__.associated_user = self.teacher
    
    def test_can_not_change_announce_when_already_true(self):
        material = self.Create_material(
            announce=True
        )
        response = self.client.patch(f"/api/teacher/material/{material.id}/", {
            "announce": False
        }, content_type="application/json")
        self.assertEqual(400, response.status_code)
