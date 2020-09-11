from ..mixins.tests import RandomLessonTextMixin
from ..models import TimeTable


class ModelTest(RandomLessonTextMixin):
    def test_timetable(self):
        lessons = self.Create_lessons()
        
        timetable = TimeTable.objects.create_with_lessons(
            lessons=lessons
        )
        
        print(timetable)
