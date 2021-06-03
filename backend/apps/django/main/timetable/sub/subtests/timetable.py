from datetime import date, timedelta

from django.core.exceptions import ValidationError

from apps.django.main.timetable.mixins import Lesson, LessonTestMixin


class TimetableModelTest(LessonTestMixin):
    def test_works_on_valid(self):
        self.Create_whole_timetable()
    
    def test_invalidates_on_overlaps(self):
        timetable = self.Create_timetable()
        
        # Valid
        self.Create_lesson(
            timetable=timetable,
            weekday=1,
            start_hour=3,
            end_hour=4
        )
        
        # Invalid exact start and end
        with self.assertRaises(ValidationError):
            self.Create_lesson(
                timetable=timetable,
                weekday=1,
                start_hour=3,
                end_hour=4
            )
        
        # Invalid start inside
        with self.assertRaises(ValidationError):
            self.Create_lesson(
                timetable=timetable,
                weekday=1,
                start_hour=4,
                end_hour=5
            )
        
        # Invalid end inside
        with self.assertRaises(ValidationError):
            self.Create_lesson(
                timetable=timetable,
                weekday=1,
                start_hour=2,
                end_hour=4
            )
        
        # Invalid start and end same
        with self.assertRaises(ValidationError):
            self.Create_lesson(
                timetable=timetable,
                weekday=1,
                start_hour=3,
                end_hour=4
            )


class StudentTimetableAPITest(LessonTestMixin):
    def setUp(self):
        self.student = self.Login_student()
        self.__class__.associated_student = self.student
        self.timetable = self.Create_whole_timetable()
    
    def test_get(self):
        response = self.client.get(f"/api/student/timetable/{self.timetable.id}/")
        self.assertStatusOk(response.status_code)
    
    def test_get_current(self):
        self.Create_whole_timetable(
            start_date=date.today() + timedelta(days=500),
            end_date=date.today() + timedelta(days=700)
        )
        self.Create_whole_timetable(
            start_date=date.today() - timedelta(days=700),
            end_date=date.today() - timedelta(days=500)
        )
        response = self.client.get("/api/student/timetable/current/")
        self.assertEqual(self.timetable.id, response.data["id"])


class TeacherTimetableAPITest(LessonTestMixin):
    def setUp(self) -> None:
        self.teacher = self.Login_teacher()
        self.student = self.Create_student_user()
        self.__class__.associated_teacher = self.teacher
        self.__class__.associated_student = self.student
        self.timetable = self.Create_whole_timetable()
    
    def test_cant_access_normal(self):
        response = self.client.get(f"/api/teacher/timetable/{self.timetable.id}/")
        self.assertEqual(404, response.status_code)
    
    def test_get_current(self):
        response = self.client.get("/api/teacher/timetable/current/")
        self.assertStatusOk(response.status_code)
        
        lessons = Lesson.objects.all().from_user(self.teacher)
        lesson_ids = lessons.values_list("id", flat=True).distinct()
        response_ids = [
            lesson["id"]
            for lesson in response.data["lessons"]
        ]
        
        self.assertCountEqual(lesson_ids, response_ids)
