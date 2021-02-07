from datetime import date

__all__ = [
    "APP_LABEL", "SCHOOL_YEAR_START_DATE", "TOKEN_LENGTH", "AVAILABLE_CLASS_NUMBERS",
    "ClassLevel", "REMEMBER_KNOWN_IP_DURATION", "STUDENT", "TEACHER"
]


class ClassLevel:
    PRIMARY = "primary"
    SECONDARY = "secondary"


APP_LABEL = "user"
SCHOOL_YEAR_START_DATE = date(1, 8, 1)
TOKEN_LENGTH = 63
AVAILABLE_CLASS_NUMBERS = range(5, 13 + 1)
REMEMBER_KNOWN_IP_DURATION = 365 * 3  # 3 years

STUDENT = "student"
TEACHER = "teacher"