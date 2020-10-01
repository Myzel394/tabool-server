import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

from apps.scooso_scrape import parser

__all__ = [
    "BaseParser"
]


@dataclass
class BaseParser(ABC):
    _raw_input: str
    _is_json: bool = False
    
    def __post_init__(self):
        self.unparsed_json = json.loads(self._raw_input) if type(self._raw_input) is str else self._raw_input
        self.json = parser.parse(self.unparsed_json)
    
    @property
    @abstractmethod
    def is_valid(self) -> bool:
        raise NotImplementedError()
    
    @property
    @abstractmethod
    def data(self):
        raise NotImplementedError()
