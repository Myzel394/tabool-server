from apps.django.utils.fields import WeekdayChoices

ALLOWED_WEEKDAYS = [
    (value, verbose)
    for value, verbose in WeekdayChoices.choices
    if value in {
        0, 1, 2, 3, 4
    }
]
