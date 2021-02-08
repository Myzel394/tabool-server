from apps.django.main.homework.mixins import ClassbookTestMixin


class ClassbookAPITest(ClassbookTestMixin):
    def setUp(self):
        self.student = self.Login_student()
        self.__class__.associated_student = self.student
        self.Create_classbook()
    
    def test_get(self):
        response = self.client.get("/api/student/classbook/")
        self.assertStatusOk(response.status_code)
