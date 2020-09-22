import json
from pprint import pp

from apps.subject.mixins.tests import LessonTestMixin
from apps.subject.serializers import LessonDataSerializer, SubjectSerializer
from apps.timetable.models import TimeTable
from apps.utils.tests import ClientTestMixin, UserCreationTestMixin
from ..subserializers import TimeTableSerializer
from ...mixins.tests.timetable import TimeTableTestMixin


class ModelTest(LessonTestMixin, UserCreationTestMixin):
    def test_timetable(self):
        lessons = set(self.Create_lessons())
        
        timetable = TimeTable.objects.create_with_lessons(
            lessons=lessons,
        )
        
        timetable_lessons = set(timetable.lessons.all())
        
        self.assertEqual(lessons, timetable_lessons, "Lessons are not equal")


# noinspection DuplicatedCode
class APITest(TimeTableTestMixin, ClientTestMixin):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
    
    def test_subject_serializer(self):
        subject = self.Create_subject()
        
        data = SubjectSerializer(subject).data
        serializer = SubjectSerializer(data=data)
        serializer.is_valid()
        
        print(serializer.validated_data)
    
    def test_single_lesson_serializer(self):
        lessons = self.Create_lesson()
        
        data = LessonDataSerializer(lessons).data
        serializer = LessonDataSerializer(data=data)
        serializer.is_valid(raise_exception=True)
    
    def test_lessons_serializer(self):
        lessons = self.Create_lessons()
        
        data = LessonDataSerializer(lessons, many=True).data
        serializer = LessonDataSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
    
    def test_timetable_serializer(self):
        timetable = self.Create_timetable()
        
        data = TimeTableSerializer(timetable).data
        
        pp(data)
    
    def test_get_all(self):
        timetable = self.Create_timetable(
            lessons=self.Create_lessons(associated_user=self.logged_user)
        )
        
        response = self.client.get("/api/timetable/")
        
        self.assertEqual(response.status_code, 200)
        actual_data = TimeTableSerializer(timetable).data
        
        self.assertEqual(json.loads(json.dumps(response.data[0])), json.loads(json.dumps(actual_data)))
    
    def test_get_single(self):
        timetable = self.Create_timetable(
            lessons=self.Create_lessons(associated_user=self.logged_user)
        )
        
        response = self.client.get(
            f"/api/timetable/{timetable.id}/"
        )
        actual_data = response.data
        expected_data = TimeTableSerializer(timetable).data
        
        self.assertEqual(actual_data, expected_data)
    
    def test_get_privacy(self):
        self.Create_timetable(
            lessons=self.Create_lessons(associated_user=self.logged_user)
        )
        self.client.logout()
        second_user = self.Login_user()
        
        response = self.client.get(
            "/api/timetable/"
        )
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.data, [])
