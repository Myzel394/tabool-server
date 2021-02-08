from apps.django.main.event.mixins import ExamTestMixin


class ExamAPITest(ExamTestMixin):
    def setUp(self):
        self.student = self.Login_student()
        self.__class__.associated_student = self.student
        self.Create_exam()
    
    def test_simple_get(self):
        response = self.client.get("/api/student/exam/")
        self.assertStatusOk(response.status_code)
