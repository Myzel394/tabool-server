from datetime import date, timedelta

from django.core.exceptions import ValidationError

from apps.django.main.homework.mixins.tests.homework import HomeworkTestMixin
from apps.django.main.homework.models import Homework, UserHomeworkRelation
from apps.utils import find_next_date_by_weekday


class ModelTest(HomeworkTestMixin):
    def test_private_to_user_validator_works(self):
        with self.assertRaises(ValidationError):
            self.Create_homework(
                private_to_user=self.Create_user()
            )


class TeacherAPITest(HomeworkTestMixin):
    def setUp(self):
        self.__class__.associated_user = self.Login_teacher()
    
    def test_can_create_public_homework(self):
        response = self.client.post("/api/teacher/homework/", {
            **self.get_lesson_argument(),
            "information": "Test"
        })
        self.assertStatusOk(response.status_code)
    
    def test_can_not_create_public_homework_via_student_api(self):
        response = self.client.post("/api/student/homework/", {
            **self.get_lesson_argument(),
            "information": "Test"
        })
        self.assertStatusNotOk(response.status_code)
    
    def test_can_create_private_homework(self):
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
    
    def test_can_edit_homework(self):
        homework = self.Create_homework()
        response = self.client.patch(f"/api/teacher/homework/{homework.id}/", {
            "information": "Blaaaa",
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)


class StudentAPITest(HomeworkTestMixin):
    def setUp(self):
        self.student = self.Login_student()
        self.__class__.associated_user = self.student
    
    def test_can_create_private_homework(self):
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
    
    def test_can_not_create_public_homework(self):
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
    
    def test_can_edit_private_homework(self):
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
    
    def test_can_not_edit_public_homework(self):
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


class StudentAPIInformationTest(HomeworkTestMixin):
    def setUp(self):
        self.student = self.Login_student()
        self.__class__.associated_user = self.student
        
        self.lesson = self.Create_lesson()
        
        self.latest_homework = self.Create_homework(
            due_date=find_next_date_by_weekday(date.today() + timedelta(days=7), self.lesson.weekday),
            lesson=self.lesson,
        )
        self.earliest_homework = self.Create_homework(
            due_date=find_next_date_by_weekday(date.today() - timedelta(days=14), self.lesson.weekday),
            lesson=self.lesson,
        )
        
        self.private_homework = self.Create_homework(
            due_date=find_next_date_by_weekday(date.today(), self.lesson.weekday),
            lesson=self.lesson,
            private_to_user=self.student
        )
        self.type_homework = self.Create_homework(
            lesson=self.lesson,
            type="Test",
        )
        
        self.completed_homework = self.Create_homework(
            due_date=find_next_date_by_weekday(date.today() - timedelta(days=14), self.lesson.weekday),
            lesson=self.lesson,
        )
        UserHomeworkRelation.objects.create(
            homework=self.completed_homework,
            completed=True,
            user=self.student
        )
        
        self.ignore_homework = self.Create_homework(
            due_date=find_next_date_by_weekday(date.today() - timedelta(days=14), self.lesson.weekday),
            lesson=self.lesson,
        )
        UserHomeworkRelation.objects.create(
            homework=self.ignore_homework,
            ignore=True,
            user=self.student
        )
    
    def test_get_information(self):
        response = self.client.get("/api/student/homework/homework-information/")
        self.assertStatusOk(response.status_code)
        data = response.data
        self.assertEqual(self.earliest_homework.due_date, data["due_date_min"])
        self.assertEqual(self.latest_homework.due_date, data["due_date_max"])
        self.assertEqual(1, data["private_count"])
        self.assertIn(self.type_homework.type, data["types"])
        self.assertEqual(1, data["completed_count"])
        self.assertEqual(1, data["ignore_count"])
