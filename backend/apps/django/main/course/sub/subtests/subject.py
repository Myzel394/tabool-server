from apps.django.main.course.mixins import SubjectTestMixin, UserTestMixin


class SubjectAPITest(SubjectTestMixin, UserTestMixin):
    def setUp(self):
        self.Login_student()
        self.Create_subject()
    
    def test_get(self):
        response = self.client.get("/api/student/subject/")
        self.assertStatusOk(response.status_code)
