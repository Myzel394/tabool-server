import json
from typing import *

from django_hint import RequestType

from . import constants


class RequestPreferredIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request: RequestType):
        if constants.PREFERRED_IDS_HEADER_NAME in request.headers and not self.is_valid(request):
            del request.headers["PREFERRED_IDS_HEADER_NAME"]
        
        response = self.get_response(request)
        
        return response
    
    @staticmethod
    def is_all_strings(elements: Iterable[str]) -> bool:
        for element in elements:
            if not type(element) is str:
                return False
        return True
    
    @classmethod
    def is_valid(cls, request: RequestType) -> bool:
        try:
            if string_data := request.headers.get(constants.PREFERRED_IDS_HEADER_NAME, ""):
                data = json.loads(string_data)
                
                if not type(data) is dict:
                    return False
                
                data: dict
                keys = data.keys()
                values = data.values()
                
                if not cls.is_all_strings(set(keys)):
                    return False
                
                for value in values:
                    if not type(value) is list:
                        return False
                    
                    if not cls.is_all_strings(value):
                        return False
                
                return True
        except Exception:
            return False
        return False
