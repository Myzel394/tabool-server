from datetime import date

__all__ = [
    "APP_LABEL", "PAY_USER_SAMPLE_AMOUNT", "SCHOOL_YEAR_START_DATE", "TOKEN_LENGTH", "AVAILABLE_CLASS_NUMBERS"
]

APP_LABEL = "authentication"
PAY_USER_SAMPLE_AMOUNT = 10
SCHOOL_YEAR_START_DATE = date(1, 8, 1)
TOKEN_LENGTH = 255
AVAILABLE_CLASS_NUMBERS = range(5, 13 + 1)
