from abc import ABC
from dataclasses import dataclass
from typing import *

from torrequest import TorRequest

from .parsers import BaseParser, LoginParser
from .. import constants
from ..exceptions import *
from ..utils import *

__all__ = [
    "Request"
]


@dataclass
class Request(ABC):
    username: str
    password: str
    session: Optional[str] = None
    
    def __post_init__(self):
        self.client = TorRequest()
        self.client.session.headers = get_headers()
    
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
                "fPassword": self.password
            }
        )
        with self.client as tr:
            for _ in range(login_attempts):
                response = tr.session.request(constants.LOGIN_CONNECTION["method"], url)
                
                parser = LoginParser(response.content)
                
                if parser.is_valid:
                    break
            else:
                raise LoginFailed()
        
        self.session = parser.data["session"]
        
        return parser.data
    
    def logout(self) -> None:
        self.session = None
    
    def request_with_parser(
            self,
            url: str,
            parser: Type[BaseParser],
            attempts: int = 5,
            data: Optional[dict] = None,
            method: str = "POST",
    ):
        data = data or {}
        full_url = build_url(url, data)
        
        with self.client as tr:
            for _ in range(attempts):
                response = tr.session.request(method, full_url)
                
                parser = parser(response.content)
                
                if parser.is_valid:
                    break
                
                # Login required
                self.login()
            else:
                raise LoginFailed()
        
        return parser.data
    
    def request(
            self,
            url: str,
            data: Optional[dict] = None,
            method: str = "POST",
    ):
        data = data or {}
        full_url = self.build_url(url, data)
        
        with self.client as tr:
            response = tr.session.request(method, full_url)
        
        return response.content
    
    @property
    def login_data(self) -> dict:
        if self.session is None:
            self.login()
        
        return {
            "logSessionId": self.session,
            "client": "rwg"
        }
