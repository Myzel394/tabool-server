from django.utils.translation import gettext_lazy as _

from apps.django.utils.translations import *

__all__ = [
    "CLASSTEST", "CLASSTEST_PLURAL", "EVENT", "EVENT_PLURAL", "MODIFICATION", "MODIFICATION_PLURAL",
    "EVENT_RELATION", "EVENT_RELATION_PLURAL"
]

CLASSTEST = _("Klassenarbeit")
CLASSTEST_PLURAL = _("Klassenarbeiten")

EVENT = _("Event")
EVENT_PLURAL = _("Events")

MODIFICATION = _("Veränderung")
MODIFICATION_PLURAL = _("Veränderungen")

EVENT_RELATION, EVENT_RELATION_PLURAL = user_relation(EVENT)
