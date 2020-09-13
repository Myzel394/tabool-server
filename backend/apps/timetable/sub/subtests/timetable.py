from apps.timetable.mixins.tests import RandomLessonTextMixin
from apps.timetable.models import TimeTable
from apps.utils.tests import ClientTestMixin, UserCreationTestMixin
from ...mixins.tests.timetable import TimeTableTestMixin
from ...serializers import LessonSerializer, TimeTableSerializer


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


class APITest(TimeTableTestMixin, ClientTestMixin):
    def setUp(self) -> None:
        self.Login_user()
    
    def test_get(self):
        self.timetable = self.Create_timetable()
        
        response = self.client.get("/api/timetable/")
        
        self.assertEqual(response.status_code, 200)
        
        real_data = TimeTableSerializer(response.data[0]).data
        test_data = TimeTableSerializer(self.timetable).data
        
        self.assertEqual(real_data, test_data)
    
    def test_create(self):
        lessons = self.Create_lessons()
        
        response = self.client.post(
            "/api/timetable/",
            {
                "lessons": LessonSerializer(lessons, many=True).data,
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
        ids = lessons.values_list("id", flat=True)
        
        response = self.client.post(
            "/api/timetable/",
            {
                "lessons": ids,
            },
            content_type="application/json"
        )
