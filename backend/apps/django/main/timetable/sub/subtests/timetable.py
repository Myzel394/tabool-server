from django.core.exceptions import ValidationError

from apps.django.main.timetable.mixins import LessonTestMixin


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


class TimetableAPITest(LessonTestMixin):
    def setUp(self):
        self.student = self.Login_student()
        self.__class__.associated_user = self.student
        self.timetable = self.Create_whole_timetable()
    
    def test_get(self):
        response = self.client.get(f"/api/student/timetable/{self.timetable.id}/")
        self.assertStatusOk(response.status_code)
