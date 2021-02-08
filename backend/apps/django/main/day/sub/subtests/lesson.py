from datetime import date, timedelta

from apps.django.main.homework.mixins import ClassbookTestMixin, HomeworkTestMixin, MaterialTestMixin
from apps.django.main.timetable.mixins import find_next_date_by_weekday


class LessonAPITest(ClassbookTestMixin, MaterialTestMixin, HomeworkTestMixin):
    def setUp(self):
        self.teacher = self.Create_teacher_user()
        self.student = self.Create_student_user()
        self.lesson = self.Create_lesson()
        self.date = find_next_date_by_weekday(date.today(), self.lesson.weekday)
        self.homework = self.Create_homework(
            lesson=self.lesson,
            lesson_date=self.date,
        )
        self.material = self.Create_material(
            lesson=self.lesson,
            lesson_date=self.date,
        )
        self.classbook = self.Create_classbook(
            lesson=self.lesson,
            lesson_date=self.date,
        )
    
    def as_student(self):
        self.lesson.course.participants.add(self.student.student)
        
        self.Login_user(self.student)
    
    def as_teacher(self):
        self.lesson.course.teacher = self.teacher.teacher
        self.lesson.course.save()
        
        self.Login_user(self.teacher)
    
    def assertContent(self, data):
        self.assertEqual(data["classbook"]["id"], self.classbook.id)
        self.assertEqual(data["materials"][0]["id"], self.material.id)
        self.assertEqual(data["homeworks"][0]["id"], self.homework.id)
    
    def student_request(self):
        response = self.client.get(
            "/api/student/lesson/",
            self.get_lesson_argument(self.lesson, self.date),
            content_type="application/json"
        )
        return response
    
    def teacher_request(self):
        response = self.client.get(
            "/api/teacher/lesson/",
            self.get_lesson_argument(self.lesson, self.date),
            content_type="application/json"
        )
        return response
    
    def test_student_can_access_student_endpoint(self):
        self.as_student()
        response = self.student_request()
        self.assertStatusOk(response.status_code)
        self.assertContent(response.data)
    
    def test_student_cant_access_teacher_endpoint(self):
        self.as_student()
        response = self.client.get(
            "/api/teacher/lesson/",
            self.get_lesson_argument(self.lesson, self.date),
            content_type="application/json"
        )
        self.assertStatusNotOk(response.status_code)
    
    def test_teacher_can_access_teacher_endpoint(self):
        self.as_teacher()
        response = self.teacher_request()
        self.assertStatusOk(response.status_code)
        self.assertContent(response.data)
    
    def test_teacher_cant_access_student_endpoint(self):
        self.as_teacher()
        response = self.client.get(
            "/api/student/lesson/",
            self.get_lesson_argument(self.lesson, self.date),
            content_type="application/json"
        )
        self.assertStatusNotOk(response.status_code)
    
    def test_invalid_date_for_lesson(self):
        self.as_student()
        response = self.client.get(
            "/api/student/lesson/",
            self.get_lesson_argument(self.lesson, self.date + timedelta(days=1)),
            content_type="application/json"
        )
        self.assertStatusNotOk(response.status_code)
