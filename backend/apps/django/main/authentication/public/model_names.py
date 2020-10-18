from django.utils.translation import gettext_lazy as _

__all__ = [
    "TOKEN", "TOKEN_PLURAL", "SCOOSO_DATA", "SCOOSO_DATA_PLURAL", "STUDENT", "STUDENT_PLURAL", "USER", "USER_PLURAL",
    "USER_PAYMENT", "USER_PAYMENT_PLURAL"
]

TOKEN = TOKEN_PLURAL = _("Token")

SCOOSO_DATA = SCOOSO_DATA_PLURAL = _("Scooso-Daten")

STUDENT = STUDENT_PLURAL = _("Schüler")

USER = USER_PLURAL = _("Benutzer")

USER_PAYMENT = _("Bezahlung")
USER_PAYMENT_PLURAL = _("Bezahlungen")