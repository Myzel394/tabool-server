from django.utils.translation import gettext_lazy as _

__all__ = [
    "scooso_data", "user_relation"
]


def scooso_data(model_name: str) -> tuple[str, str]:
    string = _("{model}-Scooso-Daten").format(model=model_name)
    
    return string, string


def user_relation(model_name: str) -> tuple[str, str]:
    return _("{model}-Benutzer-Beziehung").format(model=model_name), \
           _("{model}-Benutzer-Beziehungen").format(model=model_name)
