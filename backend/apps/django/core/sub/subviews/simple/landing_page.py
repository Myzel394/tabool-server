from django.shortcuts import render
from django_hint import RequestType

from constants import names

__all__ = [
    "landing_page"
]


def landing_page(request: RequestType):
    return render(request, "main/index.html", {
        "constants": {
            "names": names
        }
    })
