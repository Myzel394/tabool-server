from apps.django.authentication.user.mixins import UserTestMixin
from apps.django.core.constants import PRIMARY_CLASS_CONTACT_EMAIL, SECONDARY_CLASS_CONTACT_EMAIL


class ContactAPI(UserTestMixin):
    def setUp(self) -> None:
        self.user = self.Login_student()
        self.__class__.associated_student = self.user

    def change_class_number(self, class_number: int):
        student = self.user.student
        student.class_number = class_number
        student.save()

    def test_get_same_teacher(self):
        # Create teachers to stress test
        for _ in range(10):
            self.Create_teacher()

        teacher_id = self.user.student.main_teacher.user_id

        response = self.client.get("/api/student/contacts/")
        self.assertStatusOk(response.status_code)
        self.assertEqual(teacher_id, response.data["main_teacher"]["id"])

    def test_get_correct_illness_report_email_for_primary(self):
        self.change_class_number(7)

        response = self.client.get("/api/student/contacts/")
        self.assertStatusOk(response.status_code)
        self.assertEqual(PRIMARY_CLASS_CONTACT_EMAIL, response.data["illness_report_email"])

    def test_get_correct_illness_report_email_for_secondary(self):
        self.change_class_number(12)

        response = self.client.get("/api/student/contacts/")
        self.assertStatusOk(response.status_code)
        self.assertEqual(SECONDARY_CLASS_CONTACT_EMAIL, response.data["illness_report_email"])



