from apps.django.main.event import constants

__all__ = [
    "EXAM", "EVENT"
]

EXAM = f"{constants.APP_LABEL}.Exam"
EVENT = f"{constants.APP_LABEL}.Event"
