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
        with self.client as tr:
            for _ in range(login_attempts):
                response = tr.session.request(constants.LOGIN_CONNECTION["method"], url, headers=get_headers())
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
    ):
        with self.client as tr:
            for _ in range(attempts):
                data = get_data()
                url = data.pop("url")
                headers = get_headers()
                headers.update(data.pop("headers", {}))
                
                """
                request = requests.Request(url=url, headers=headers, **data)
                prepared = request.prepare()
                print_request(prepared)"""
                
                response = tr.session.request(url=url, headers=headers, **data)
                
                if response.status_code == 200:
                    parser_instance = parser_class(response.content)
                    
                    if parser_instance.is_valid:
                        break
                
                # Maybe session is not valid anymore
                self.login()
            else:
                raise RequestFailed()
        
        return parser_instance.data
    
    @property
    def login_data(self) -> dict:
        return {
            "logSessionId": self.session,
            "client": "rwg",
            "logUserIe": self.second_session_data,
            "sc_version": 6,
            "institution": "rwg"
        }
