from urllib import parse

__all__ = [
    "build_url", "get_headers"
]

from requests.utils import default_headers


def build_url(url: str, data: dict) -> str:
    return f"{url}?{parse.urlencode(data)}"


def get_headers() -> dict:
    headers = default_headers()
    headers[
        "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                        "Chrome/85.0.4183.102 Safari/537.36"
    
    return headers
