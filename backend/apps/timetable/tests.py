import json
from datetime import date, datetime, timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from rest_framework import status

from .models import Lesson, Room, Subject, Teacher, TimeTable
from .serializers import LessonSerializer
from .utils import create_designation_from_date
from ..utils.fields.weekday import WeekdayChoices
from ..utils.tests import StartTimeEndTimeTestMixin, UserCreationTestMixin
from ..utils.time import dummy_datetime_from_time


class ModelTest(UserCreationTestMixin, StartTimeEndTimeTestMixin):
    def setUp(self) -> None:
        self.user = self.create_user()
        
        self.teacher = Teacher.objects.create(
            first_name="Midel",
            last_name="Traschnitschi",
        )
        self.subject = Subject.objects.create(
            name="Mathe",
            color="#ed3454",
        )
        self.room = Room.objects.create(
            place="A45"
        )
        
        self.lesson = Lesson.objects.create(
            start_time=self.start_time,
            end_time=self.end_time,
            subject=self.subject,
            teacher=self.teacher,
            room=self.room,
            weekday=0,
        )
    
    def test_room(self):
        Room.objects.create(
            place="A45"
        )
        Room.objects.create(
            place="B001"
        )
        Room.objects.create(
            place="Halle"
        )
        Room.objects.create(
            place="Nebenraum"
        )
        
        should_raise = ["900 Halle", "", "-ö_-"]
        
        for element in should_raise:
            self.assertRaises(ValidationError, lambda: Room.objects.create(place=element))
    
    def test_lesson(self):
        assert self.lesson.duration == self.DURATION, "Duration is wrong"
        
        Lesson.objects.create(
            start_time=self.start_time,
            end_time=self.end_time,
            subject=self.subject,
            weekday=1
        )
    
    def test_lesson_relation(self):
        assert list(self.teacher.lessons) == list(self.room.lessons) == list(self.subject.lessons)
    
    def test_create_timetable(self):
        WEEKDAY = WeekdayChoices.Friday
        now = datetime.now()
        lessons = []
        
        for index, subject in enumerate([
            Subject.objects.create(
                name="Mathe",
                color="#ed3454",
            ),
            Subject.objects.create(
                name="Musik",
                color="#FEFF06"
            ),
            Subject.objects.create(
                name="Deutsch",
                color="#2861D4"
            ),
            Subject.objects.create(
                name="Englisch",
                color="#107CFF"
            )
        ]):
            start_time = (now + timedelta(minutes=self.DURATION * index)).time()
            end_time = (dummy_datetime_from_time(start_time) + timedelta(minutes=self.DURATION)).time()
            lesson = Lesson.objects.create(
                start_time=start_time,
                end_time=end_time,
                weekday=WEEKDAY,
                teacher=self.teacher,
                subject=subject,
                room=self.room
            )
            
            lessons.append(lesson)
        
        timetable = TimeTable.Easy_create(
            lessons=lessons,
            associated_user=self.user,
        )
        
        timetable_lessons = timetable.lessons.all()
        
        print(timetable_lessons)


class ApiTest(TestCase):
    client = Client()
    DURATION = 45
    start_time = datetime.now().time()
    end_time = (dummy_datetime_from_time(start_time) + timedelta(minutes=DURATION)).time()
    
    def setUp(self) -> None:
        self.user = User.objects.create(username="Myzel394", first_name="Miguel", last_name="Krasniqi")
        
        self.lesson = Lesson.objects.create(
            start_time=self.start_time,
            end_time=self.end_time,
            teacher=Teacher.objects.create(
                first_name="Frank",
                last_name="Marker"
            ),
            room=Room.objects.create(
                place="118"
            ),
            subject=Subject.objects.create(
                name="Musik",
            ),
        )
    
    def test_all_lesson(self):
        response = self.client.get("/api/timetable/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = json.loads(response.content)
        
        self.assertEqual(data, LessonSerializer(Lesson.objects.all(), many=True).data)
    
    def test_single_lesson(self):
        lesson = Lesson.objects.all()[0]
        lesson_id = lesson.id
        
        response = self.client.get(f"/api/timetable/{lesson_id}/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = json.loads(response.content)
        
        self.assertEqual(data, LessonSerializer(lesson).data)
    
    def test_create_lesson(self):
        self.client.post(f"/api/timetable/", json.dumps({
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "teacher": {
                "first_name": "Adrian",
                "last_name": "Herbst"
            },
            "room": {
                "place": "110"
            },
            "subject": {
                "name": "Musik"
            }
        }), content_type="application/json")


class UtilsTest(TestCase):
    def test_designation_creation(self):
        today = date(day=1, month=10, year=2020)
        expected = "2. Halbjahr 2020"
        
        self.assertEqual(create_designation_from_date(today), expected)
        
        today2 = date(day=1, month=1, year=2020)
        expected2 = "1. Halbjahr 2020"
        
        self.assertEqual(create_designation_from_date(today2), expected2)
