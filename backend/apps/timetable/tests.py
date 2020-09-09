import json
from datetime import date, datetime, timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from rest_framework import status

from .models import Lesson, Room, Subject, Teacher, TimeTable
from .serializers import LessonSerializer
from .utils import create_designation_from_date
from ..lesson.mixins.tests import RandomLessonTextMixin
from ..utils.tests import ClientTestMixin, StartTimeEndTimeTestMixin, UserCreationTestMixin
from ..utils.time import dummy_datetime_from_time


class ModelTest(UserCreationTestMixin, RandomLessonTextMixin):
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
        
        self.lesson = self.Create_lesson()
    
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
    
    def test_lesson_relation(self):
        assert list(self.teacher.lessons) == list(self.room.lessons) == list(self.subject.lessons)
    
    def test_create_timetable(self):
        lessons = self.Create_lessons()
        lessons = set(lessons)
        
        timetable = TimeTable.Easy_create(
            lessons=lessons,
            associated_user=self.user,
        )
        
        timetable_lessons = timetable.lessons.all()
        timetable_lessons = set(timetable_lessons)
        
        self.assertEqual(lessons, timetable_lessons, "Lessons are not equal")


class ApiTest(TestCase):
    client = Client()
    DURATION = 45
    start_time = datetime.now().time()
    end_time = (dummy_datetime_from_time(start_time) + timedelta(minutes=DURATION)).time()
    
    def setUp(self) -> None:
        self.user = User.objects.create(username="Myzel394", first_name="Miguel", last_name="Krasniqi")
        
        self.lesson = Lesson.objects.create(
            start_time=self.start_time(),
            end_time=self.end_time(),
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
            "start_time": self.start_time().isoformat(),
            "end_time": self.end_time().isoformat(),
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


class ApiTest(UserCreationTestMixin, StartTimeEndTimeTestMixin, ClientTestMixin):
    def setUp(self):
        timetable = TimeTable.Easy_create(
            lessons=[
                Lesson.objects.create(
                
                )
            ]
        )


class UtilsTest(TestCase):
    def test_designation_creation(self):
        today = date(day=1, month=10, year=2020)
        expected = "2. Halbjahr 2020"
        
        self.assertEqual(create_designation_from_date(today), expected)
        
        today2 = date(day=1, month=1, year=2020)
        expected2 = "1. Halbjahr 2020"
        
        self.assertEqual(create_designation_from_date(today2), expected2)
