from datetime import date, timedelta

from django.core.exceptions import ValidationError

from apps.timetable.models import Lesson, Room, Subject, Teacher
from apps.utils.tests import StartTimeEndTimeTestMixin, UserCreationTestMixin
from .models import Homework
from ..utils.fields.weekday import WeekdayChoices


class ModelTest(UserCreationTestMixin, StartTimeEndTimeTestMixin):
    def setUp(self) -> None:
        self.teacher = Teacher.objects.create(
            first_name="Frank",
            last_name="Marker"
        )
        
        self.subject = Subject.objects.create(
            name="Musik",
        )
        
        self.room = Room.objects.create(
            place="118"
        )
        
        self.lesson = Lesson.objects.create(
            start_time=self.start_time(),
            end_time=self.end_time(),
            teacher=self.teacher,
            room=self.room,
            subject=self.subject,
            weekday=WeekdayChoices.Monday
        )
    
    def test_creation(self):
        Homework.objects.create(
            subject=self.subject,
            description="Noten lesen",
        )
        Homework.objects.create(
            subject=self.subject,
            description="Noten lesen",
            due_date=date.today() + timedelta(days=5),
            completed=True,
        )
        
        self.assertRaises(ValidationError, lambda: Homework.objects.create(
            subject=self.subject,
            due_date=date.today() - timedelta(days=2),
            description="Test"
        ))
    
    def test_complete(self):
        homework = Homework.objects.create(
            subject=self.subject,
            description="Noten lesen",
        )
        
        homework.complete()
        
        self.assertEqual(homework.completed, True)
