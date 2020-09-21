from apps.utils.fields.weekday import WeekdayChoices

APP_LABEL = "subject"
LESSON_ALLOWED_DAYS = [
    choice
    for choice in WeekdayChoices.choices
    if choice[0] in {
        0, 1, 2, 3, 4
    }
]
