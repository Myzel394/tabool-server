from datetime import date, timedelta

from apps.lesson.mixins.tests import LessonTestMixin
from apps.lesson.mixins.tests.associated_user import AssociatedUserTestMixin
from apps.lesson.models import Lesson
from apps.lesson.serializers import LessonListSerializer
from apps.timetable.models import Timetable
from apps.utils.tests import ClientTestMixin, UserCreationTestMixin
from ..subserializers import TimetableDetailSerializer
from ...mixins.tests.timetable import TimetableTestMixin


class ModelTest(LessonTestMixin, UserCreationTestMixin):
    def test_timetable(self):
        lessons = set(self.Create_lessons_data())
        
        timetable = Timetable.objects.create_with_lessons(
            lessons_data=lessons,
        )
        
        timetable_lessons = set(timetable.lessons_data.all())
        
        self.assertEqual(lessons, timetable_lessons, "Lessons are not equal")


# noinspection DuplicatedCode
class APITest(TimetableTestMixin, ClientTestMixin):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
        self.__class__.associated_user = self.logged_user
    
    def test_get_single(self):
        timetable = self.Create_timetable()
        
        expected_data = TimetableDetailSerializer(timetable).data
        response = self.client.get(
            f"/api/timetable/{timetable.id}/"
        )
        actual_data = response.data
        
        self.assertCountEqual(actual_data, expected_data)
    
    def test_get_privacy(self):
        self.Create_timetable()
        self.client.logout()
        self.Login_user()
        
        response = self.client.get(
            "/api/timetable/"
        )
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.data["results"], [])
    
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
        
        self.assertStatusOk(response.status_code)
        
        self.assertCountEqual(
            response.data,
            LessonListSerializer(Lesson.objects.from_user(self.logged_user), many=True).data
        )


class QuerySetTest(TimetableTestMixin, AssociatedUserTestMixin):
    def test_association(self):
        self.check_queryset_from_user(Timetable)
