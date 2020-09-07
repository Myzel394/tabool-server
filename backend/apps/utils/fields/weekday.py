from django.db import models
from django.utils.translation import gettext_lazy as _


class WeekdayChoices(models.IntegerChoices):
    Monday = 0, _("Montag")
    Tuesday = 1, _("Dienstag")
    Wednesday = 2, _("Mittwoch")
    Thursday = 3, _("Donnerstag")
    Friday = 4, _("Freitag")
    Saturday = 5, _("Samstag")
    Sunday = 6, _("Sonntag")


class WeekdayField(models.PositiveSmallIntegerField):
    description = _("Feld für einen Wochentag")
    
    def __init__(self, *args, **kwargs):
        kwargs["choices"] = kwargs.get("choices") or WeekdayChoices.choices
        
        super().__init__(*args, **kwargs)
