from django.utils.translation import gettext_lazy as _

__all__ = [
    "CHOICE_NAME", "CHOICE_NAME_PLURAL", "POLL_NAME", "POLL_NAME_PLURAL", "VOTE", "VOTE_PLURAL"
]

CHOICE_NAME = _("Auswahl")
CHOICE_NAME_PLURAL = _("Auswahlen")

POLL_NAME = _("Umfrage")
POLL_NAME_PLURAL = _("Umfragen")

VOTE = _("Abstimmung")
VOTE_PLURAL = _("Abstimmungen")
