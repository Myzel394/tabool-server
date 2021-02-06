from datetime import date

from apps.django.main.homework.mixins import ClassbookTestMixin, HomeworkTestMixin, MaterialTestMixin
from apps.django.main.timetable.mixins import find_next_date_by_weekday


class StudentAPITest(ClassbookTestMixin, MaterialTestMixin, HomeworkTestMixin):
    def setUp(self):
        self.user = self.Login_student()
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
    
    def test_student_get(self):
        response = self.client.get(
            "/api/student/lesson/",
            self.get_lesson_argument(self.lesson, self.date),
            content_type="application/json"
        )
        self.assertStatusOk(response.status_code)
        self.assertEqual(response.data["classbook"]["id"], self.classbook.id)
        self.assertEqual(response.data["materials"][0]["id"], self.material.id)
        self.assertEqual(response.data["homeworks"][0]["id"], self.homework.id)
    
    def test_teacher_cant_access(self):
        self.Login_teacher()
        response = self.client.get(
            "/api/student/lesson/",
            self.get_lesson_argument(self.lesson, self.date),
            content_type="application/json"
        )
        self.assertStatusNotOk(response.status_code)
