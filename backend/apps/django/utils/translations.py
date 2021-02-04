from django.utils.translation import gettext_lazy as _

__all__ = [
    "user_relation"
]


def user_relation(model_name: str) -> tuple[str, str]:
    return _("{model}-Benutzer-Beziehung").format(model=model_name), \
           _("{model}-Benutzer-Beziehungen").format(model=model_name)
