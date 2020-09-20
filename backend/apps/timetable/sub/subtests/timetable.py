import json

from apps.timetable.mixins.tests import RandomLessonTextMixin
from apps.timetable.models import TimeTable
from apps.utils.tests import ClientTestMixin, UserCreationTestMixin
from ...mixins.tests.timetable import TimeTableTestMixin
from ...serializers import LessonSerializer, SubjectSerializer, TimeTableSerializer


class ModelTest(RandomLessonTextMixin, UserCreationTestMixin):
    def test_timetable(self):
        lessons = set(self.Create_lessons())
        user = self.Create_user()
        
        timetable = TimeTable.objects.create_with_lessons(
            lessons=lessons,
            associated_user=user
        )
        
        timetable_lessons = set(timetable.lessons.all())
        
        self.assertEqual(lessons, timetable_lessons, "Lessons are not equal")


# noinspection DuplicatedCode
class APITest(TimeTableTestMixin, ClientTestMixin):
    def setUp(self) -> None:
        self.Login_user()
    
    def test_subject_serializer(self):
        subject = self.Create_subject()
        
        data = SubjectSerializer(subject).data
        serializer = SubjectSerializer(data=data)
        serializer.is_valid()
        
        print(serializer.validated_data)
    
    def test_single_lesson_serializer(self):
        lessons = self.Create_lesson()
        
        data = LessonSerializer(lessons).data
        serializer = LessonSerializer(data=data)
        serializer.is_valid()
        
        print(serializer.is_valid())
    
    def test_lessons_serializer(self):
        lessons = self.Create_lessons()
        
        data = LessonSerializer(lessons, many=True).data
        serializer = LessonSerializer(data=data, many=True)
        serializer.is_valid()
        
        print(serializer.is_valid())
    
    def test_get(self):
        self.timetable = self.Create_timetable()
        
        response = self.client.get("/api/timetable/")
        
        self.assertEqual(response.status_code, 200)
        actual_data = TimeTableSerializer(self.timetable).data
        
        self.assertEqual(json.loads(json.dumps(response.data[0])), json.loads(json.dumps(actual_data)))
    
    def test_create(self):
        lessons = self.Create_lessons()
        data = LessonSerializer(lessons, many=True).data
        
        response = self.client.post(
            "/api/timetable/",
            {
                "lessons": data,
            },
            content_type="application/json"
        )
        
        self.assertStatusOk(response.status_code)
        
        timetable = TimeTable.objects.all().first()
        
        actual_data = response.data
        expected_data = TimeTableSerializer(timetable).data
        
        self.assertEqual(actual_data, expected_data)
    
    def test_create_id(self):
        lessons = self.Create_lessons()
        ids = [
            {
                "id": lesson.id
            }
            for lesson in lessons
        ]
        
        response = self.client.post(
            "/api/timetable/",
            {
                "lessons": ids,
            },
            content_type="application/json"
        )
        
        self.assertStatusOk(response.status_code)
        
        timetable = TimeTable.objects.all().first()
        
        actual_data = response.data
        expected_data = TimeTableSerializer(timetable).data
        
        self.assertEqual(actual_data, expected_data)
