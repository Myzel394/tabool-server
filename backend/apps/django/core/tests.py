from apps.django.core.constants import PRIMARY_CLASS_CONTACT_EMAIL, SECONDARY_CLASS_CONTACT_EMAIL
from apps.django.main.authentication.models import Student
from apps.django.main.school_data.mixins.tests import TeacherTestMixin
from apps.django.utils.tests import ClientTestMixin, UserTestMixin


class ContactAPI(UserTestMixin, TeacherTestMixin, ClientTestMixin):
    def create_student(self, class_number: int = 10):
        self.teacher = self.Create_teacher()
        
        Student.objects.create(
            user=self.user,
            main_teacher=self.teacher,
            class_number=class_number
        )
    
    def setUp(self) -> None:
        self.user = self.Login_user()
        self.__class__.associated_user = self.user
    
    def test_get_same_teacher(self):
        # Create teachers to stress test
        for _ in range(10):
            self.Create_teacher()
            
        self.create_student()
        
        response = self.client.get("/api/data/contacts/")
        self.assertStatusOk(response.status_code)
        self.assertEqual(self.teacher.id, response.data["main_teacher"]["id"])
    
    def test_get_correct_illness_report_email_for_primary(self):
        self.create_student(7)
        
        response = self.client.get("/api/data/contacts/")
        self.assertStatusOk(response.status_code)
        self.assertEqual(PRIMARY_CLASS_CONTACT_EMAIL, response.data["illness_report_email"])
    
    def test_get_correct_illness_report_email_for_secondary(self):
        self.create_student(12)
        
        response = self.client.get("/api/data/contacts/")
        self.assertStatusOk(response.status_code)
        self.assertEqual(SECONDARY_CLASS_CONTACT_EMAIL, response.data["illness_report_email"])
        
        

