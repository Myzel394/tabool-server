from apps.django.main.homework.mixins.tests.homework import HomeworkTestMixin
from apps.django.main.homework.models import Homework


class TeacherAPITest(HomeworkTestMixin):
    def setUp(self):
        self.__class__.associated_user = self.Login_teacher()
    
    def test_teacher_can_create_public_homework(self):
        response = self.client.post("/api/teacher/homework/", {
            **self.get_lesson_argument(),
            "information": "Test"
        })
        self.assertStatusOk(response.status_code)
    
    def test_teacher_can_not_create_public_homework_via_student_api(self):
        response = self.client.post("/api/student/homework/", {
            **self.get_lesson_argument(),
            "information": "Test"
        })
        self.assertStatusNotOk(response.status_code)
    
    def test_teacher_can_create_private_homework(self):
        self.student = self.Create_student_user()
        lesson = self.Create_lesson(
            course=self.Create_course(
                participants=[self.student]
            )
        )
        
        response = self.client.post("/api/teacher/homework/", {
            **self.get_lesson_argument(lesson),
            "information": "Test",
            "private_to_user": self.student.id
        })
        self.assertStatusOk(response.status_code)
        
        homework = Homework.objects.all()[0]
        
        self.assertEqual(self.student, homework.private_to_user)
    
    def test_teacher_can_edit_homework(self):
        homework = self.Create_homework()
        response = self.client.patch(f"/api/teacher/homework/{homework.id}/", {
            "information": "Blaaaa",
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)


class StudentAPITest(HomeworkTestMixin):
    def setUp(self):
        self.student = self.Login_student()
        self.__class__.associated_user = self.student
    
    def test_user_can_create_private_homework(self):
        lesson = self.Create_lesson(
            course=self.Create_course(
                participants=[self.student]
            )
        )
        
        response = self.client.post("/api/student/homework/", {
            **self.get_lesson_argument(lesson),
            "information": "Test",
            "is_private": True
        })
        self.assertStatusOk(response.status_code)
    
    def test_user_can_not_create_public_homework(self):
        lesson = self.Create_lesson(
            course=self.Create_course(
                participants=[self.student]
            )
        )
        
        response = self.client.post("/api/student/homework/", {
            **self.get_lesson_argument(lesson),
            "information": "Test",
            "is_private": False
        })
        self.assertStatusOk(response.status_code)
    
    def test_student_can_edit_private_homework(self):
        lesson = self.Create_lesson(
            course=self.Create_course(
                participants=[self.student]
            )
        )
        
        homework = self.Create_homework(
            private_to_user=self.student,
            lesson=lesson,
        )
        response = self.client.patch(f"/api/student/homework/{homework.id}/", {
            "information": "Blaaaa",
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
    
    def test_student_can_not_edit_public_homework(self):
        lesson = self.Create_lesson(
            course=self.Create_course(
                participants=[self.student]
            )
        )
        
        homework = self.Create_homework(
            private_to_user=None,
            lesson=lesson,
        )
        response = self.client.patch(f"/api/student/homework/{homework.id}/", {
            "information": "Blaaaa",
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)
