from django.test import TestCase

from ..mixins.tests import RandomLessonTextMixin


class ModelTest(RandomLessonTextMixin):
    def test_timetable(self):
        lessons = self.Create_lessons()
        
        

