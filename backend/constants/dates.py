from datetime import date, datetime, time

from django.utils.translation import gettext_lazy as _

__all__ = [
    "FORMATS"
]

FORMATS = {
    # Translators: Formatierung für Daten (Datum). Befehle: https://strftime.org/
    date.__name__: _("%d.%m.%Y"),
    # Translators: Formatierung für Daten + Uhrzeiten (Datum + Uhrzeit). Befehle: https://strftime.org/
    datetime.__name__: _("%d.%m.%Y, %H:%M"),
    # Translators: Formatierung für Uhrzeiten (Uhrzeit). Befehle: https://strftime.org/
    time.__name__: _("%H:%M")
}
