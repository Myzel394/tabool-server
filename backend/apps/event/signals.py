from django.db.models.signals import post_save
from django.dispatch import receiver
from django_eventstream import send_event
from simple_history.signals import pre_create_historical_record

from .models import Classtest, Modification
from .public import *
from ..history_extras.extras.user_information.setter import set_user_information


@receiver(pre_create_historical_record)
def set_homework_historical_user_information(instance: Classtest, **kwargs):
    if isinstance(instance, Classtest):
        set_user_information(**kwargs)


@receiver(post_save, sender=Modification)
def modification_send_sse(instance: Modification, created, **kwargs):
    if created:
        send_event(MODIFICATION_CHANNEL, "modification", {
            "course_id": instance.course_id
        })
