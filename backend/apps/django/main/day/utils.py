from datetime import date, timedelta

__all__ = [
    "get_date"
]


def get_date() -> date:
    targeted_date = date.today()
    weekday = targeted_date.weekday()

    if weekday >= 5:
        targeted_date += timedelta(days=7 - weekday)

    return targeted_date
