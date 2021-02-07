from apps.django.main.event.mixins import ModificationTestMixin


class ModificationAPITest(ModificationTestMixin):
    def setUp(self):
        self.student = self.Login_student()
        self.__class__.associated_user = self.student
        self.Create_modification()
    
    def test_simple_get(self):
        response = self.client.get("/api/student/modification/")
        self.assertStatusOk(response.status_code)
