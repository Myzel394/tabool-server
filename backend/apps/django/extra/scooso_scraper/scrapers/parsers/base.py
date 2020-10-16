import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

import chardet

from apps.django.extra.scooso_scraper import parser

__all__ = [
    "BaseParser"
]


@dataclass
class BaseParser(ABC):
    _raw_input: bytes
    _is_json: bool = False
    
    @staticmethod
    def decode_data(data: bytes) -> str:
        codec = chardet.detect(data)["encoding"]
        
        if codec is None:
            return data.decode("utf-8")
        return data.decode(codec)
    
    def __post_init__(self):
        if type(self._raw_input) is bytes:
            data = self.decode_data(self._raw_input)
        else:
            data = self._raw_input
        
        self.unparsed_json = json.loads(data) if type(data) is str else data
        self.json = parser.parse(self.unparsed_json)
    
    @property
    @abstractmethod
    def is_valid(self) -> bool:
        raise NotImplementedError()
    
    @property
    @abstractmethod
    def data(self):
        raise NotImplementedError()
