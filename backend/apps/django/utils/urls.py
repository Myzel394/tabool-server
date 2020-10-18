from django.urls import include, path

__all__ = [
    "build_patterns"
]


def build_url(prefix: str) -> str:
    return f"api/{prefix}/"


def build_patterns(prefix: str, url_list: list[str]) -> list:
    return [
        path(build_url(prefix), include(urls))
        for urls in url_list
    ]
