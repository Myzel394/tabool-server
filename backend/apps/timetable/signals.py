from typing import *

from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.timetable.models import TimeTable


@receiver(pre_save)
def validate_timetable_lessons(instance: TimeTable, sender: Type[TimeTable]) -> None:
    print("YAÄÄI PRe SÄÄIVE")
    print(instance)
