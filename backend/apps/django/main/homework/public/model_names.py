from django.utils.translation import gettext_lazy as _

from apps.django.utils.translations import user_relation

__all__ = [
    "HOMEWORK", "HOMEWORK_PLURAL", "MATERIAL", "MATERIAL_PLURAL", "HOMEWORK_RELATION", "HOMEWORK_RELATION_PLURAL"
]

HOMEWORK = _("Hausaufgabe")
HOMEWORK_PLURAL = _("Hausaufgaben")

MATERIAL = _("Material")
MATERIAL_PLURAL = _("Materialien")

SUBMISSION = _("Einsendung")
SUBMISSION_PLURAL = _("Einsendungen")

CLASSBOOK = _("Klassenbuch")
CLASSBOOK_PLURAL = _("Klassenbücher")

HOMEWORK_RELATION, HOMEWORK_RELATION_PLURAL = user_relation(HOMEWORK)
