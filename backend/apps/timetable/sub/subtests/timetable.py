import json
from datetime import date, timedelta
from pprint import pp

from apps.lesson.mixins.tests import LessonTestMixin
from apps.lesson.mixins.tests.associated_user import AssociatedUserTestMixin
from apps.lesson.models import Lesson
from apps.lesson.serializers import LessonDataDetailSerializer, LessonListSerializer, SubjectDetailSerializer
from apps.timetable.models import Timetable
from apps.utils.tests import ClientTestMixin, UserCreationTestMixin
from ..subserializers import TimetableDetailSerializer, TimetableListSerializer
from ...mixins.tests.timetable import TimetableTestMixin


class ModelTest(LessonTestMixin, UserCreationTestMixin):
    def test_timetable(self):
        lessons = set(self.Create_lessons_data())
        
        timetable = Timetable.objects.create_with_lessons(
            lessons_data=lessons,
        )
        
        timetable_lessons = set(timetable.lessons_data.all())
        
        self.assertEqual(lessons, timetable_lessons, "Lessons are not equal")


# TODO: Remove unnecessary tests

# noinspection DuplicatedCode
class APITest(TimetableTestMixin, ClientTestMixin):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
        self.__class__.associated_user = self.logged_user
    
    def test_subject_serializer(self):
        subject = self.Create_subject()
        
        data = SubjectDetailSerializer(subject).data
        serializer = SubjectDetailSerializer(data=data)
        serializer.is_valid()
        
        print(serializer.validated_data)
    
    def test_single_lesson_serializer(self):
        lessons = self.Create_lesson_data()
        
        data = LessonDataDetailSerializer(lessons).data
        serializer = LessonDataDetailSerializer(data=data)
        serializer.is_valid(raise_exception=True)
    
    def test_lessons_serializer(self):
        lessons = self.Create_lessons_data()
        
        data = LessonDataDetailSerializer(lessons, many=True).data
        serializer = LessonDataDetailSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
    
    def test_timetable_serializer(self):
        timetable = self.Create_timetable()
        
        data = TimetableDetailSerializer(timetable).data
        
        pp(data)
    
    def test_get_all(self):
        timetable = self.Create_timetable()
        
        response = self.client.get("/api/timetable/")
        
        self.assertEqual(response.status_code, 200)
        actual_data = TimetableListSerializer(timetable).data
        
        self.assertEqual(json.loads(json.dumps(response.data[0])), json.loads(json.dumps(actual_data)))
    
    def test_get_single(self):
        timetable = self.Create_timetable()
        
        response = self.client.get(
            f"/api/timetable/{timetable.id}/"
        )
        actual_data = response.data
        expected_data = TimetableDetailSerializer(timetable).data
        
        self.assertEqual(actual_data, expected_data)
    
    def test_get_privacy(self):
        self.Create_timetable()
        self.client.logout()
        second_user = self.Login_user()
        
        response = self.client.get(
            "/api/timetable/"
        )
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.data, [])
    
    def test_lesson_creation(self):
        timetable = self.Create_timetable()
        
        response = self.client.get(
            f"/api/timetable/{timetable.id}/lessons/",
            {
                "start_date": date.today(),
                "end_date": date.today() + timedelta(days=3)
            },
            content_type="application/json"
        )
        
        print(response.data)
        self.assertStatusOk(response.status_code)
        
        self.assertCountEqual(
            response.data,
            LessonListSerializer(Lesson.objects.all().from_user(self.logged_user), many=True).data
        )


# TODO: AssociatedUser zu Timetable ändern! (Subjects hat jeder)
# TODO: add User Preferences app!


class QuerySetTest(TimetableTestMixin, AssociatedUserTestMixin):
    def test_association(self):
        self.check_queryset_from_user(Timetable)
