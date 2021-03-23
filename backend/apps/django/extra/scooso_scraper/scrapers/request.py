import json
import random
from dataclasses import dataclass
from typing import *

import requests
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from torrequest import TorRequest

from constants.request_generator import generate_session
from .parsers import BaseParser, LoginParser
from .. import constants
from ..exceptions import *
from ..models import ScoosoRequest
from ..utils import *

__all__ = [
    "Request"
]

from ..utils import print_request


@dataclass
class Request:
    username: str
    password: str
    session: Optional[str] = None
    second_session_data: Optional[str] = None
    
    def __post_init__(self):
        self.client = TorRequest()
    
    def __enter__(self):
        self.login()
        
        return self
    
    def __exit__(self, *args, **kwargs):
        self.logout()
    
    @staticmethod
    def create_underscore() -> int:
        number = random.randint(0, 100_000_000)
        number -= number % 43
        
        return number
    
    @staticmethod
    def _print_request(encoding: str = "ascii", **kwargs) -> None:
        request = requests.Request(**kwargs)
        prepared = request.prepare()
        
        if type(prepared.body) is bytes:
            prepared.body = prepared.body.decode(encoding)
        
        print_request(prepared)
    
    @staticmethod
    def _minify_to_json(data: Union[list, dict]) -> str:
        return json.dumps(
            data,
            separators=(",", ":"),
            cls=DjangoJSONEncoder,
            default=str
        )
    
    @classmethod
    def _store_request(cls, raw_response: str, attempts: int, identifier: str, request_data: dict):
        minified_request = cls._minify_to_json(request_data)
        
        ScoosoRequest.objects.create(
            name=identifier,
            attempts_required=attempts,
            response=raw_response,
            request_data=minified_request
        )
    
    # Utils
    
    def build_url(self, url: str, data: dict) -> str:
        use_data = data.copy()
        use_data.update(self.login_data)
        
        return build_url(url, use_data)
    
    def login(self, login_attempts: int = 5) -> dict:
        url = build_url(
            constants.LOGIN_CONNECTION["url"], {
                "fInstitution": "rwg",
                "fUsername": self.username,
                "fPassword": self.password,
                "asd": "Anmelden"
            }
        )
        session, _ = generate_session("Login")
        for _ in range(login_attempts):
            response = session.request(constants.LOGIN_CONNECTION["method"], url, headers=get_headers())
            content = response.content.decode("utf-8")
            
            parser = LoginParser(content)
            
            if parser.is_valid:
                break
        else:
            raise LoginFailed()
        
        self.session = parser.data["session"]
        self.second_session_data = parser.data["second_session_data"]
        
        if type(self.second_session_data) is list:
            self.second_session_data = self.second_session_data[0]
        
        return parser.data
    
    def logout(self) -> None:
        self.session = None
    
    def request_with_parser(
            self,
            parser_class: Type[BaseParser],
            get_data: Callable,
            attempts: int = 8,
            user_agent_name: Optional[str] = None,
            store_in_database: bool = True
    ):
        session, identifier = generate_session(user_agent_name)
        
        for _ in range(attempts):
            data = get_data()
            url = data.pop("url")
            headers = get_headers()
            headers.update(data.pop("headers", {}))
            
            if settings.DEBUG:
                self._print_request(url=url, headers=headers, **data)
            
            response = session.request(url=url, headers=headers, **data)
            
            if response.status_code == 200:
                scooso_content = response.content
                
                parser_instance = parser_class(scooso_content)
                
                if parser_instance.is_valid:
                    break
            
            # Maybe session is not valid anymore
            self.login()
        else:
            raise RequestFailed()
        
        if store_in_database:
            try:
                self._store_request(
                    raw_response=scooso_content,
                    request_data={
                        **data,
                        "url": url,
                    },
                    attempts=attempts,
                    identifier=identifier
                )
            except Exception as e:
                pass
        
        return parser_instance.data
    
    @property
    def login_data(self) -> dict:
        return {
            "logSessionId": self.session,
            "client": "rwg",
            "logUserIe": self.second_session_data,
        }
