from .mixins.tests import RandomLessonTextMixin


class ModelTest(RandomLessonTextMixin):
    def setUp(self) -> None:
        self.lesson = self.Create_lesson()
