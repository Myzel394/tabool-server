import random
from datetime import date

from apps.django.main.event.mixins import ExamTestMixin, ModificationTestMixin
from apps.django.main.homework.mixins import ClassbookTestMixin, HomeworkTestMixin, MaterialTestMixin
from apps.django.main.timetable.models import Lesson
from apps.utils import find_next_date_by_weekday


class DailyDataMixin(ExamTestMixin, HomeworkTestMixin, ClassbookTestMixin, ModificationTestMixin, MaterialTestMixin):
    @property
    def random_lesson(self) -> tuple[Lesson, date]:
        lesson = random.choice(self.lessons)
        targeted_date = find_next_date_by_weekday(date.today(), lesson.weekday)
        
        return lesson, targeted_date
    
    def setUp(self) -> None:
        self.teacher = self.Create_teacher_user()
        self.student = self.Create_student_user()
        self.__class__.associated_student = self.student
        self.__class__.associated_teacher = self.teacher
        self.lessons = [
            self.Create_lesson()
            for _ in range(20)
        ]
        lesson, targeted_date = self.random_lesson
        self.homework = self.Create_homework(
            lesson=lesson,
            lesson_date=targeted_date
        )
        lesson, targeted_date = self.random_lesson
        self.modification = self.Create_classbook(
            lesson=lesson,
            lesson_date=targeted_date
        )
        lesson, targeted_date = self.random_lesson
        self.modification = self.Create_modification(
            lesson=lesson,
            lesson_date=targeted_date
        )
        lesson, targeted_date = self.random_lesson
        self.material = self.Create_material(
            lesson=lesson,
            lesson_date=targeted_date,
        )


class StudentDailyDataAPITest(DailyDataMixin):
    def setUp(self) -> None:
        super().setUp()
        self.Login_user(self.student)
    
    def test_get_invalid_date(self):
        targeted_date = find_next_date_by_weekday(date.today(), 5)
        response = self.client.get("/api/student/daily-data/", {
            "date": targeted_date,
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)
    
    def test_get_lesson(self):
        lesson, targeted_date = self.random_lesson
        
        response = self.client.get("/api/student/daily-data/", {
            "date": targeted_date,
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
        
        lesson_ids = [
            lesson["id"]
            for lesson in response.data["lessons"]
        ]
        self.assertIn(lesson.id, lesson_ids)
    
    def test_get_homework(self):
        targeted_date = self.homework.lesson_date
        
        response = self.client.get("/api/student/daily-data/", {
            "date": targeted_date,
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
        
        homework_ids = [
            homework["id"]
            for homework in response.data["homeworks"]
        ]
        self.assertIn(self.homework.id, homework_ids)
