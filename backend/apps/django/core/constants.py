from apps.django.main.authentication.constants import ClassLevel

__all__ = [
    "PRIMARY_CLASS_CONTACT_EMAIL", "SECONDARY_CLASS_CONTACT_EMAIL", "CONTACT_MAIL_MAP"
]

PRIMARY_CLASS_CONTACT_EMAIL = "sekretariat@rwg-neuwied.de"
SECONDARY_CLASS_CONTACT_EMAIL = "mss-buero@rwg-neuwied.de"

CONTACT_MAIL_MAP = {
    ClassLevel.PRIMARY: PRIMARY_CLASS_CONTACT_EMAIL,
    ClassLevel.SECONDARY: SECONDARY_CLASS_CONTACT_EMAIL
}
