from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Request(ABC):
    client: int  # TODO: client!
    
    def login(self, username: str, password: str):
        pass
    
    def request(self, retry_amount: int = 3, relogin: bool = True):
        pass
    
    @abstractmethod
    def download_data(self):
        raise NotImplementedError()
    
    @abstractmethod
    def parse_data(self):
        raise NotImplementedError()
    
    @abstractmethod
    def data_valid(self, data) -> bool:
        raise NotImplementedError()
    
