from typing import *

from django.test import Client, TestCase

__all__ = [
    "ClientTestMixin", "joinkwargs",
]


class ClientTestMixin(TestCase):
    client = Client()
    
    def assertStatusOk(self, status_code: int) -> None:
        self.assertTrue(200 <= status_code <= 299, f"status_code is '{status_code}'")
    
    def assertStatusNotOk(self, status_code: int) -> None:
        self.assertTrue(status_code < 200 or status_code > 299, f"status_code is '{status_code}'")


def joinkwargs(defaults: Dict[str, Callable], given: dict, /) -> dict:
    data = {}
    for key, value in defaults.items():
        if key in given:
            data[key] = given[key]
        else:
            data[key] = value()
    
    remaining_keys = set(given.keys()) - set(defaults.keys())
    
    for key in remaining_keys:
        data[key] = given[key]
    
    return data
