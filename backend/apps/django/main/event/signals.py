from django.dispatch import receiver
from simple_history.signals import pre_create_historical_record

from apps.django.utils.history_extras.extras.user_information.setter import set_user_information
from .models import Exam


@receiver(pre_create_historical_record)
def set_homework_historical_user_information(instance: Exam, **kwargs):
    if isinstance(instance, Exam):
        set_user_information(**kwargs)
