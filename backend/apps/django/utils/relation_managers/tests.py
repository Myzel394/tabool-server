from apps.django.main.lesson.mixins.tests import LessonTestMixin


class CallTest(LessonTestMixin):
    def test_dummy(self):
        self.Create_lesson()
