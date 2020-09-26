from apps.utils.fields.weekday import WeekdayChoices

ALLOWED_WEEKDAYS = [
    choice
    for choice in WeekdayChoices.choices
    if choice[0] in {
        0, 1, 2, 3, 4
    }
]