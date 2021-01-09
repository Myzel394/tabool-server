from dataclasses import dataclass

from .base import BaseParser


@dataclass
class MaterialUploadParser(BaseParser):
    @property
    def is_valid(self) -> bool:
        try:
            self.json["item"]["file_id"]
            return True
        except:
            return False
    
    @property
    def data(self):
        return self.json["item"]["file_id"]
