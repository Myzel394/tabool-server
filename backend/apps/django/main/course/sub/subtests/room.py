from apps.django.main.course.mixins import RoomTestMixin, UserTestMixin


class RoomAPITest(RoomTestMixin, UserTestMixin):
    def setUp(self):
        self.Login_student()
        self.Create_room()

    def test_get(self):
        response = self.client.get("/api/student/room/")
        self.assertStatusOk(response.status_code)
