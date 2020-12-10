from apps.django.main.lesson import constants

__all__ = [
    "COURSE", "LESSON", "LESSON_DATA"
]

COURSE = f"{constants.APP_LABEL}.Course"
LESSON = f"{constants.APP_LABEL}.Lesson"
LESSON_DATA = f"{constants.APP_LABEL}.LessonData"
LESSON_CONTENT = f"{constants.APP_LABEL}.LessonContent"
