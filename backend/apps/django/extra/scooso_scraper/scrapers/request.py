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
    
    def __post_init__(self):
        self.client = TorRequest()
        self.client.session.headers = get_headers()
    
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
                response = tr.session.request(constants.LOGIN_CONNECTION["method"], url)
                content = response.content.decode("utf-8")
                
                parser = LoginParser(content)
                
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
            parser_class: Type[BaseParser],
            get_data: Callable,
            attempts: int = 8,
    ):
        with self.client as tr:
            for _ in range(attempts):
                data = get_data()
                url = data.pop("url")
                
                """ Debugging
                request = requests.Request(url=url, **data)
                prepared = request.prepare()
                print_request(prepared)"""
                
                response = tr.session.request(url=url, **data)
                
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
            "sc_version": 6,
        }
