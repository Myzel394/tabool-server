from apps.django.main.event.mixins import EventTestMixin


class EventAPITest(EventTestMixin):
    def setUp(self):
        self.student = self.Login_student()
        self.__class__.associated_user = self.student
        self.Create_event()
    
    def test_simple_get(self):
        response = self.client.get("/api/student/event/")
        self.assertStatusOk(response.status_code)
