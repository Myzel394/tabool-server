from django.urls import include, path

from constants.api import API_VERSION

__all__ = [
    "build_patterns"
]


def build_url(prefix: str) -> str:
    return f"api/{API_VERSION}/{prefix}/"


def build_patterns(prefix: str, url_list: list[str]) -> list:
    return [
        path(build_url(prefix), include(urls))
        for urls in url_list
    ]
