from apps.django.main.homework.mixins.tests import HomeworkTestMixin
from apps.django.utils.tests import *


class HistoryTest(HomeworkTestMixin, ClientTestMixin):
    def test_history(self):
        homework = self.Create_homework()
        homework.information = "First Edit!"
        homework.save()
        homework.information = "Second Edit!"
        homework.save()
        
        prev_record = homework.prev_record
        latest = homework.history.latest()
        
        print()
