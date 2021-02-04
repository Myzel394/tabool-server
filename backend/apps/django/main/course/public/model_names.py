from django.utils.translation import gettext_lazy as _

from apps.django.utils.translations import user_relation

__all__ = [
    "ROOM", "ROOM_PLURAL", "SUBJECT", "SUBJECT_PLURAL", "COURSE", "COURSE_PLURAL", "SUBJECT_RELATION",
    "SUBJECT_RELATION_PLURAL"
]

ROOM = _("Raum")
ROOM_PLURAL = _("Räume")

SUBJECT = _("Fach")
SUBJECT_PLURAL = _("Fächer")

COURSE = _("Kurs")
COURSE_PLURAL = _("Kurse")

SUBJECT_RELATION, SUBJECT_RELATION_PLURAL = user_relation(SUBJECT)
