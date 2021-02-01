from typing import *
from datetime import date, datetime, time, timedelta

from django.test import TestCase

from apps.utils import is_all_day


class DateText(TestCase):
    def assertIsAllDay(self, first: Union[date, datetime], second: Union[date, datetime]):
        self.assertTrue(is_all_day(first, second))
    
    def test_same_date_zero(self):
        first_date = datetime(2020, 1, 1, 0, 0, 0)
        second_date = datetime(2020, 1, 1, 0, 0, 0)
        
        self.assertIsAllDay(first_date, second_date)
    
    def test_same_date_min_max(self):
        first_date = datetime.combine(date(2020, 1, 1), time.min)
        second_date = datetime.combine(date(2020, 1, 1), time.max)
        
        self.assertIsAllDay(first_date, second_date)
    
    def test_same_date_exactly_24_hours(self):
        first_date = datetime(2020, 1, 1, 0, 0, 0)
        second_date = first_date + timedelta(hours=24)
        
        self.assertIsAllDay(first_date, second_date)
    
    def test_not_same_date(self):
        first_date = datetime(2020, 1, 1, 0, 0, 0)
        second_date = first_date + timedelta(hours=1)
        
        self.assertFalse(is_all_day(first_date, second_date))
