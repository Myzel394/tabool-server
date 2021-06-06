from django.core.exceptions import ValidationError

from apps.django.authentication.user.mixins import STUDENT, TEACHER, UserTestMixin


class CreationTest(UserTestMixin):
    def setUp(self):
        self.user = self.Create_user(confirm_email=False)

    def test_student_cant_create_when_user_not_confirmed(self):
        with self.assertRaises(ValidationError):
            self.Create_student(user=self.user)

    def test_teacher_cant_create_when_user_confirmed(self):
        with self.assertRaises(ValidationError):
            self.Create_teacher(user=self.user)

    def test_student_cant_change_user(self):
        student = self.Create_student_user().student

        with self.assertRaises(ValidationError):
            student.user = self.Create_user()
            student.save()

    def test_teacher_cant_change_user(self):
        teacher = self.Create_teacher_user().teacher

        with self.assertRaises(ValidationError):
            teacher.user = self.Create_user()
            teacher.save()


class TypeTest(UserTestMixin):
    def test_get_correct_type_and_bool_for_user(self):
        user = self.Create_student_user()

        self.assertEqual(user.user_type, STUDENT)
        self.assertTrue(user.is_student)

    def test_get_correct_type_and_bool_for_teacher(self):
        user = self.Create_teacher_user()

        self.assertEqual(user.user_type, TEACHER)
        self.assertTrue(user.is_teacher)
