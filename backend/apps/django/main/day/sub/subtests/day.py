from datetime import date, datetime, time, timedelta

from apps.django.main.event.mixins import ExamTestMixin, ModificationTestMixin
from apps.django.main.event.mixins.tests.event import EventTestMixin
from apps.django.main.homework.mixins import ClassbookTestMixin, MaterialTestMixin
from apps.utils import find_next_date_by_weekday


class Mixin(ClassbookTestMixin, MaterialTestMixin, EventTestMixin, ModificationTestMixin, ExamTestMixin):
    def setUp(self):
        self.teacher = self.Create_teacher_user()
        self.student = self.Create_student_user()
        self.lesson = self.Create_lesson()
        self.date = find_next_date_by_weekday(date.today(), self.lesson.weekday)
        self.material = self.Create_material(
            lesson=self.lesson,
            lesson_date=self.date,
        )
        self.event = self.Create_event(
            start_datetime=datetime.combine(self.date, time.min),
            end_datetime=datetime.combine(self.date, time.min) + timedelta(hours=2)
        )
        self.modification = self.Create_modification(
            lesson=self.lesson,
            lesson_date=self.date,
        )
        self.exam = self.Create_exam(
            date=self.date,
            course=self.lesson.course
        )
    
    def as_student(self):
        self.lesson.course.participants.add(self.student)
        
        self.Login_user(self.student)
    
    def as_teacher(self):
        self.lesson.course.teacher = self.teacher.teacher
        self.lesson.course.save()
        
        self.Login_user(self.teacher)
    
    def assertContent(self, data):
        self.assertEqual(data["lessons"][0]["id"], self.lesson.id)
        self.assertEqual(data["materials"][0]["id"], self.material.id)
        self.assertEqual(data["events"][0]["id"], self.event.id)
        self.assertEqual(data["modifications"][0]["id"], self.modification.id)
        self.assertEqual(data["exams"][0]["id"], self.exam.id)


class StudentAPITest(Mixin):
    def test_get_in_range(self):
        self.as_student()
        response = self.client.get("/api/student/day/", {
            "start_date": self.date - timedelta(days=1),
            "end_date": self.date + timedelta(days=1)
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
        self.assertContent(response.data)
    
    def test_get_not_in_range(self):
        self.as_student()
        response = self.client.get("/api/student/day/", {
            "start_date": self.date - timedelta(days=300),
            "end_date": self.date - timedelta(days=299)
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
        self.assertEqual(0, sum(len(element) for element in response.data.values()))
    
    def test_get_invalid_dates(self):
        self.as_student()
        response = self.client.get("/api/student/day/", {
            "start_date": self.date + timedelta(days=3),
            "end_date": self.date - timedelta(days=1)
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)
    
    def test_student_cant_access_teacher_endpoint(self):
        self.as_student()
        response = self.client.get("/api/teacher/day/", {
            "start_date": self.date - timedelta(days=1),
            "end_date": self.date + timedelta(days=1)
        }, content_type="application/json")
        self.assertEqual(403, response.status_code)
    
    def test_date_autofill(self):
        self.as_student()
        response = self.client.get("/api/student/day/")
        self.assertStatusOk(response.status_code)


class TeacherAPITest(Mixin):
    def test_get_in_range(self):
        self.as_teacher()
        response = self.client.get("/api/teacher/day/", {
            "start_date": self.date - timedelta(days=1),
            "end_date": self.date + timedelta(days=1)
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
        self.assertContent(response.data)
    
    def test_get_not_in_range(self):
        self.as_teacher()
        response = self.client.get("/api/teacher/day/", {
            "start_date": self.date - timedelta(days=300),
            "end_date": self.date - timedelta(days=299)
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
        self.assertEqual(0, sum(len(element) for element in response.data.values()))
    
    def test_get_invalid_dates(self):
        self.as_teacher()
        response = self.client.get("/api/teacher/day/", {
            "start_date": self.date + timedelta(days=3),
            "end_date": self.date - timedelta(days=1)
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)
    
    def test_teacher_cant_access_student_endpoint(self):
        self.as_teacher()
        response = self.client.get("/api/student/day/", {
            "start_date": self.date - timedelta(days=1),
            "end_date": self.date + timedelta(days=1)
        }, content_type="application/json")
        self.assertEqual(403, response.status_code)
