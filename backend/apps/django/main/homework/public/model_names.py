from django.utils.translation import gettext_lazy as _

from apps.django.utils.translations import *

__all__ = [
    "HOMEWORK", "HOMEWORK_PLURAL", "MATERIAL", "MATERIAL_PLURAL", "SUBMISSION", "SUBMISSION_PLURAL",
    "MATERIAL_SCOOSO", "MATERIAL_SCOOSO_PLURAL", "SUBMISSION_SCOOSO", "SUBMISSION_SCOOSO_PLURAL",
    "HOMEWORK_RELATION", "HOMEWORK_RELATION_PLURAL"
]

HOMEWORK = _("Hausaufgabe")
HOMEWORK_PLURAL = _("Hausaufgaben")

MATERIAL = _("Material")
MATERIAL_PLURAL = _("Materialien")

SUBMISSION = _("Einreichung")
SUBMISSION_PLURAL = _("Einreichungen")

MATERIAL_SCOOSO, MATERIAL_SCOOSO_PLURAL = scooso_data(MATERIAL)

SUBMISSION_SCOOSO, SUBMISSION_SCOOSO_PLURAL = scooso_data(SUBMISSION)

HOMEWORK_RELATION, HOMEWORK_RELATION_PLURAL = user_relation(HOMEWORK)