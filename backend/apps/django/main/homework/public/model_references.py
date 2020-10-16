from apps.django.main.homework import constants

__all__ = [
    "HOMEWORK", "MATERIAL", "SUBMISSION"
]

HOMEWORK = f"{constants.APP_LABEL}.Homework"
MATERIAL = f"{constants.APP_LABEL}.Material"
SUBMISSION = f"{constants.APP_LABEL}.Submission"
