from apps.django.main.lesson import constants

__all__ = [
    "COURSE", "LESSON"
]

COURSE = f"{constants.APP_LABEL}.Course"
LESSON = f"{constants.APP_LABEL}.Lesson"
LESSON_CONTENT = f"{constants.APP_LABEL}.LessonContent"
