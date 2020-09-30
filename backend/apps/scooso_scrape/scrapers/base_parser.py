import json
from dataclasses import dataclass

from .. import parser


@dataclass
class BaseParser:
    _raw_json: str
    
    def __post_init__(self):
        self.unparsed_json = json.loads(self._raw_json)
        self.json = parser.parse(self.unparsed_json)
    