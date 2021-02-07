from apps.django.main.homework.mixins import MaterialTestMixin


class APITest(MaterialTestMixin):
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
