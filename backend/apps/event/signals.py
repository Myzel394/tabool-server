from django.dispatch import receiver
from simple_history.signals import pre_create_historical_record

from .models import Classtest
from ..history_extras.extras.user_information.setter import set_user_information


@receiver(pre_create_historical_record)
def set_homework_historical_user_information(instance: Classtest, **kwargs):
    if isinstance(instance, Classtest):
        set_user_information(**kwargs)